from configparser import ConfigParser
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_cors import CORS
from sqlalchemy import MetaData, func, distinct
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.automap import automap_base, name_for_scalar_relationship, name_for_collection_relationship
from collections import defaultdict
from sqlalchemy import and_
from Configuration.Config import config

INVOICE_PER_PAGE = 100
CONTRACT_PER_PAGE = 100

app = Flask(__name__)

#Vyresi Cross Origin Resource Sharing
CORS(app)

#Dokumentace - diky kodu nize se generuje API dokumentace na adrese /
api = Api(app, version='1.0', title='Matcher API',
    description='Matcher API documentation')
ns_st = api.namespace('statistics', description='Statistics of database data')
ns_invoices = api.namespace('invoices', description='Invoices operations')
ns_contracts = api.namespace('contracts', description='Contracts operations')
ns_relations = api.namespace('relations', description='Relations operations')
ns_warnings = api.namespace('warnings', description='Warnings operations')
ns_ministry = api.namespace('ministry', description='Ministry operations')

db_congig = config("matcherdb")

#Databaze - pristup k databazi, namapovani tabulek
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_congig["user"]}:{db_congig["password"]}@{db_congig["host"]}/{db_congig["database"]}'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
metadata = MetaData()
metadata.reflect(db.engine, only=['invoice', 'contract', 'test_result', 'possible_relation', 'statistics', 'ministry', 'contract_warning'])
Base = automap_base(metadata=metadata)
Base.prepare(name_for_scalar_relationship=name_for_scalar_relationship, name_for_collection_relationship=name_for_collection_relationship)

Invoice = Base.classes.invoice
Contract = Base.classes.contract
TestResult = Base.classes.test_result
PossibleRelation = Base.classes.possible_relation
Statistics = Base.classes.statistics
Ministry = Base.classes.ministry
ContractWarning = Base.classes.contract_warning

#Routes
@ns_st.route('/', methods=['GET'])
class Statistics_Route(Resource):
    def get(self):
        """
        Returns statistics about the data in the database
        (num of invoices, contracts, linked invoices, warnings, date data were refreshed)
        :return: Dict[str, str]
        """
        inv_count = db.session.query(Statistics.int_attribute).filter(Statistics.type == "num_of_invoices")
        con_count = db.session.query(Statistics.int_attribute).filter(Statistics.type == "num_of_contracts")
        rel_count = db.session.query(Statistics.int_attribute).filter(Statistics.type == "num_of_linked")
        warning_count = db.session.query(Statistics.int_attribute).filter(Statistics.type == "num_of_warnings")
        refreshed = db.session.query(Statistics.date_attribute).filter(Statistics.type == "num_of_warnings")

        res = jsonify(invoice_count=inv_count[0][0],
                      contract_count=con_count[0][0],
                      linked_count=rel_count[0][0],
                      warnings_count=warning_count[0][0],
                      refreshed=refreshed[0][0].strftime('%d.%m.%Y'))
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_ministry.route('/', methods=['GET'])
class MinistryPage(Resource):
    def get(self):
        """
        Returns list of ministries and coresponding ICO
        :return: Dict[str, str]
        """
        try:
            ministry_list = db.session.query(Ministry)

            serializer = lambda m: {
                              "ministry_name":m.ministry_name,
                              "ministry_ico":m.ministry_ico
                          }
            result_list = [serializer(m) for m in ministry_list]
        except OperationalError:
            result_list = []

        res = jsonify(ministry=result_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_invoices.route('/page', methods=['GET'])
class InvoicesPage(Resource):

    @ns_invoices.doc(params={'page': 'Number of page we want to return',
                             'm_ico': 'ICO of the ministry',
                             's_ico': 'ICO of the supplier',
                             's_name': 'Name of the supplier',
                             'from': 'Date from which we want to show data. Format: YYYY-MM-DD.',
                             'to': 'Date till which we want to show data. Format: YYYY-MM-DD.',
                             'linked': '''Boolean value. 
                                          'True' if we want to return only linked. 
                                          'False' if we want to return only records without link.
                                          Blank if we want to return all records.
                                       '''},
                     responses={200: 'Success',
                                400: 'Page number is not valid'})
    def get(self):
        """
        Return list of invoices (specific page)
        :return: Dist[str, List]
        """
        page = request.args.get('page', default=1, type=int)
        m_ico = request.args.get('m_ico', default=None, type=str)
        s_ico = request.args.get('s_ico', default=None, type=str)
        s_name = request.args.get('s_name', default=None, type=str)
        d_from = request.args.get('from', default=None, type=str)
        d_to = request.args.get('to', default=None, type=str)
        linked = request.args.get('linked', default=None, type=str)

        if page < 1:
            abort(400, "Page parameter have to be greater then zero")
        try:
            query = db.session.query(Invoice, func.count(PossibleRelation.possible_relation_id))\
                    .outerjoin(PossibleRelation, and_(PossibleRelation.invoice_id == Invoice.invoice_id, PossibleRelation.real == True))
            if d_from is not None:
                query = query.filter(Invoice.date_issue >= d_from)
            if d_to is not None:
                query = query.filter(Invoice.date_issue <= d_to)
            if m_ico is not None:
                query = query.filter(Invoice.ministry_ico == m_ico)
            if s_name is not None:
                query = query.filter(Invoice.supplier_name.ilike(s_name + "%"))
            if s_ico is not None:
                query = query.filter(Invoice.supplier_ico == s_ico)
            query = query.group_by(Invoice)
            if linked is not None and linked == 'true':
                query = query.having(func.count(PossibleRelation.possible_relation_id) != 0)
            elif linked is not None and linked == 'false':
                query = query.having(func.count(PossibleRelation.possible_relation_id) == 0)

            print("test")
            invoice_list = query.order_by(Invoice.invoice_id.desc()).paginate(page, per_page=INVOICE_PER_PAGE, error_out=False).items
            print("test2")
            serializer = lambda i: {"invoice_id":i[0].invoice_id,
                                  "ministry_name":i[0].ministry_name,
                                  "supplier_name":i[0].supplier_name,
                                  "purpose": i[0].purpose,
                                  "date_issue":i[0].date_issue.strftime('%d.%m.%Y'),
                                  "amount": max([i for i in [i[0].amount_with_dph, i[0].amount_without_dph] if i is not None], default= 0),
                                  "linked": True if i[1] is not 0 and i[1] is not None else False}
            result_list = [serializer(i) for i in invoice_list]
            print(result_list)
        except OperationalError:
            result_list = []

        res = jsonify(invoices=result_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_contracts.route('/page', methods=['GET'])
class ContractsPage(Resource):

    @ns_contracts.doc(params={'page': 'Number of page we want to return',
                             'm_ico': 'ICO of the ministry',
                             's_ico': 'ICO of the supplier',
                             's_name': 'Name of the supplier',
                             'from': 'Date from which we want to show data. Format: YYYY-MM-DD.',
                             'to': 'Date till which we want to show data. Format: YYYY-MM-DD.',
                             'linked': '''Boolean value. 
                                          'True' if we want to return only linked. 
                                          'False' if we want to return only records without link.
                                          Blank if we want to return all records.
                                       '''},
                     responses={200: 'Success',
                                400: 'Page number is not valid'})
    def get(self):
        """
        Return list of contracts (specific page)
        :return: Dist[str, List]
        """
        page = request.args.get('page', default=1, type=int)
        m_ico = request.args.get('m_ico', default=None, type=str)
        s_ico = request.args.get('s_ico', default=None, type=str)
        s_name = request.args.get('s_name', default=None, type=str)
        d_from = request.args.get('from', default=None, type=str)
        d_to = request.args.get('to', default=None, type=str)
        linked = request.args.get('linked', default=None, type=str)

        if page < 1:
            abort(400, "Page parameter have to be greater then zero")

        try:
           query = db.session.query(Contract, func.count(distinct(PossibleRelation.possible_relation_id)))\
               .outerjoin(PossibleRelation, and_(PossibleRelation.contract_id == Contract.contract_id, PossibleRelation.real == True))
           if d_from is not None:
               query = query.filter(Contract.date_agreed >= d_from)
           if d_to is not None:
               query = query.filter(Contract.date_agreed <= d_to)
           if m_ico is not None:
               query = query.filter(Contract.ministry_ico == m_ico)
           if s_name is not None:
               query = query.filter(Contract.supplier_name.ilike(s_name + "%"))
           if s_ico is not None:
               query = query.filter(Contract.supplier_ico == s_ico)
           query = query.group_by(Contract)
           if linked is not None and linked == 'true':
               query = query.having(func.count(PossibleRelation.possible_relation_id) != 0)
           elif linked is not None and linked == 'false':
               query = query.having(func.count(PossibleRelation.possible_relation_id) == 0)
           contract_list = query.order_by(Contract.contract_id).paginate(page, per_page=CONTRACT_PER_PAGE).items

           serializer = lambda c: {"contract_id":c[0].contract_id,
                                  "ministry_name":c[0].ministry_name,
                                  "supplier_name":c[0].supplier_name,
                                  "purpose": c[0].purpose,
                                  "date_agreed": c[0].date_agreed.strftime('%d.%m.%Y'),
                                  "amount": max([i for i in [c[0].amount_with_dph, c[0].amount_without_dph] if i is not None], default=None),
                                  "linked": c[1] if c[1] is not None else None}
           result_list = [serializer(c) for c in contract_list]
        except OperationalError:
           result_list = []

        print(len(result_list))
        res = jsonify(contracts=result_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_warnings.route('/page', methods=['GET'])
class WarningsPage(Resource):

    @ns_warnings.doc(params={'page': 'Number of page we want to return',
                              'm_ico': 'ICO of the ministry',
                              's_ico': 'ICO of the supplier',
                              's_name': 'Name of the supplier',
                              'from': 'Date from which we want to show data. Format: YYYY-MM-DD.',
                              'to': 'Date till which we want to show data. Format: YYYY-MM-DD.'},
                     responses={200: 'Success',
                                400: 'Page number is not valid'})
    def get(self):
        """
        Return list of warnings (specific page)
        :return: Dist[str, List]
        """
        page = request.args.get('page', default=1, type=int)
        m_ico = request.args.get('m_ico', default=None, type=str)
        s_ico = request.args.get('s_ico', default=None, type=str)
        s_name = request.args.get('s_name', default=None, type=str)
        d_from = request.args.get('from', default=None, type=str)
        d_to = request.args.get('to', default=None, type=str)

        if page < 1:
            abort(400, "Page parameter have to be greater then zero")

        try:
            query = db.session.query(Contract, ContractWarning.difference).join(ContractWarning, ContractWarning.contract_id == Contract.contract_id)
            if d_from is not None:
                query = query.filter(Contract.date_issue >= d_from)
            if d_to is not None:
                query = query.filter(Contract.date_issue <= d_to)
            if m_ico is not None:
                query = query.filter(Contract.ministry_ico == m_ico)
            if s_name is not None:
                query = query.filter(Contract.supplier_name.ilike(s_name + "%"))
            if s_ico is not None:
                query = query.filter(Contract.supplier_ico == s_ico)
            contract_list = query.order_by(Contract.contract_id.desc()).paginate(page, per_page=CONTRACT_PER_PAGE).items

            serializer = lambda c: {"contract_id":c[0].contract_id,
                                  "ministry_name":c[0].ministry_name,
                                  "supplier_name":c[0].supplier_name,
                                  "purpose": c[0].purpose,
                                  "date_agreed": c[0].date_agreed.strftime('%d.%m.%Y'),
                                  "amount": max([i for i in [c[0].amount_with_dph, c[0].amount_without_dph] if i is not None]),
                                  "difference": c.difference
                                  }
            result_list = [serializer(c) for c in contract_list]
        except OperationalError:
            result_list = []

        res = jsonify(contracts=result_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_invoices.route('/<int:invoice_id>', methods=['GET'])
class Invoice_route(Resource):
    def get(self, invoice_id):
        """
        Return invoice details
        :return: Dist[str, str]
        """
        try:
            invoice_list = db.session.query(Invoice).filter(Invoice.invoice_id == invoice_id)

            serializer = lambda i: {"invoice_id": i.invoice_id,
            "external_id": i.external_id,
            "ministry_ico": i.ministry_ico,
            "ministry_name": i.ministry_name,
            "supplier_ico": i.supplier_ico,
            "supplier_name": i.supplier_name,
            "amount_with_dph": i.amount_with_dph,
            "amount_per_item": i.amount_per_item,
            "amount_without_dph": i.amount_without_dph,
            "amount_different_currency": i.amount_different_currency,
            "currency": i.currency,
            "purpose": i.purpose,
            "supplier_invoice_identifier": i.supplier_invoice_identifier,
            "document_label": i.document_label,
            "document_number": i.document_number,
            "variable_symbol": i.variable_symbol,
            "date_acceptance": i.date_acceptance.strftime('%d.%m.%Y') if i.date_acceptance is not None else None,
            "date_payment": i.date_payment.strftime('%d.%m.%Y') if i.date_acceptance is not None else None,
            "date_due": i.date_due.strftime('%d.%m.%Y') if i.date_due is not None else None,
            "date_issue": i.date_issue.strftime('%d.%m.%Y') if i.date_issue is not None else None,
            "budget_item_code": i.budget_item_code,
            "budget_item_name": i.budget_item_name,
            "contract_identifier": i.contract_identifier}

            result_list = [serializer(i) for i in invoice_list]
        except OperationalError:
            result_list = []

        if result_list:
            invoice = result_list[0]
        else:
            invoice = None
        res = jsonify(invoice=invoice)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_contracts.route('/<int:contract_id>', methods=['GET'])
class Contract_route(Resource):
    def get(self, contract_id):
        """
        Return contract details
        :return: Dist[str, str]
        """
        try:
            contract_list = db.session.query(Contract).filter(Contract.contract_id == contract_id)

            serializer = lambda c: {
                "contract_id": c.contract_id,
                "external_id": c.external_id,
                "version_id": c.version_id,
                "link": c.link,
                "date_published": c.date_published,
                "ministry_name": c.ministry_name,
                "ministry_data_box": c.ministry_data_box,
                "ministry_ico": c.ministry_ico,
                "ministry_address": c.ministry_address,
                "ministry_department": c.ministry_department,
                "ministry_payer_flag": c.ministry_payer_flag,
                "supplier_name": c.supplier_name,
                "supplier_date_box": c.supplier_date_box,
                "supplier_ico": c.supplier_ico,
                "supplier_address": c.supplier_address,
                "supplier_department": c.supplier_department,
                "supplier_receiver_flag": c.supplier_receiver_flag,
                "purpose": c.purpose,
                "date_agreed": c.date_agreed,
                "contract_number": c.contract_number,
                "approved": c.approved,
                "amount_without_dph": c.amount_without_dph,
                "amount_with_dph": c.amount_with_dph,
                "amount_different_currency": c.amount_different_currency,
                "currency": c.currency,
                "valid": c.valid,
                "linked_record": c.linked_record,
            }

            result_list = [serializer(i) for i in contract_list]
        except OperationalError:
            result_list = []

        if result_list:
            contract = result_list[0]
        else:
            contract = None
        res = jsonify(contract=contract)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_st.route('/invoices_monthly', methods=['GET'])
class InvoiceMonthlyStats(Resource):
    def get(self):
        """
        Return number of invoices per month. Data are divided to two lists.
        :return: Dist[str, List]
        """
        try:
            qlist = db.session.query(Statistics.text_attribute, Statistics.int_attribute).filter(Statistics.type == "num_invoices_per_month").order_by(Statistics.text_attribute)

            serializer = lambda i: {"month": i.text_attribute, "invoice_count": i.int_attribute}
            month_list = [serializer(i)["month"] for i in qlist]
            count_list = [serializer(i)["invoice_count"] for i in qlist]
        except OperationalError:
            month_list = []
            count_list = []

        res = jsonify(months=month_list, invoice_count=count_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_st.route('/contracts_monthly', methods=['GET'])
class ContractsMonthlyStats(Resource):
    def get(self):
        """
        Return number of contracts per month. Data are divided to two lists.
        :return: Dist[str, List]
        """
        try:
            qlist = db.session.query(Statistics.text_attribute, Statistics.int_attribute).filter(Statistics.type == "num_contracts_per_month").order_by(Statistics.text_attribute)

            serializer = lambda i: {"month": i.text_attribute, "contract_count": i.int_attribute}
            month_list = [serializer(i)["month"] for i in qlist]
            count_list = [serializer(i)["contract_count"] for i in qlist]
        except OperationalError:
            month_list = []
            count_list = []

        res = jsonify(months=month_list, contract_count=count_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


def get_contracts_monthly_stats_per_ministry():
    """
    Return number of contracts per ministry.
    :return: Dist[str, Dict]
    """
    try:
        mlist = db.session.query(Ministry)
        qlist = db.session.query(Statistics.type, Statistics.text_attribute, Statistics.text_attribute_2, Statistics.int_attribute).filter(Statistics.type == "num_contracts_per_month_ministry").order_by(Statistics.text_attribute_2)

        val_dict = defaultdict(list)
        res_dict = defaultdict(dict)

        for q in qlist:
            val_dict[q.text_attribute].append({"month": q.text_attribute_2, "contract_count": q.int_attribute})

        for m in mlist:
            values = val_dict[m.shortcut]
            counts = [x["contract_count"] for x in values]
            months = [x["month"] for x in values]
            res_dict[m.shortcut] = {"months": months, "counts": counts}

    except OperationalError:
        res_dict = {}
    return res_dict


def get_invoices_monthly_stats_per_ministry():
    """
    Return number of invoices per ministry.
    :return: Dist[str, Dict]
    """
    try:
        mlist = db.session.query(Ministry)
        qlist = db.session.query(Statistics.type, Statistics.text_attribute, Statistics.text_attribute_2, Statistics.int_attribute).filter(Statistics.type == "num_invoices_per_month_ministry").order_by(Statistics.text_attribute_2)

        val_dict = defaultdict(list)
        res_dict = defaultdict(dict)

        for q in qlist:
            val_dict[q.text_attribute].append({"month": q.text_attribute_2, "invoices_count": q.int_attribute})

        for m in mlist:
            values = val_dict[m.shortcut]
            counts = [x["invoices_count"] for x in values]
            months = [x["month"] for x in values]
            res_dict[m.shortcut] = {"months": months, "counts": counts}

    except OperationalError:
        res_dict = {}
    return res_dict


@ns_st.route('/ministry_data', methods=['GET'])
class MinistryData(Resource):
    def get(self):
        """
        Return statistics per ministry
        :return: Dist[str, List]
        """
        reslist = []

        mlist = db.session.query(Ministry)
        ministeries = defaultdict(dict)

        for m in mlist:
            ministeries[m.shortcut] = {"ministry_name": m.ministry_name, "ministry_ico": m.ministry_ico}

        contract_data = get_contracts_monthly_stats_per_ministry()

        for key, value in contract_data.items():
            mdict = ministeries[key]
            mdict["contract_count_monthly"] = value

        invoices_data = get_invoices_monthly_stats_per_ministry()

        for key, value in invoices_data.items():
            mdict = ministeries[key]
            mdict["invoice_count_monthly"] = value

        clist = db.session.query(Statistics.type, Statistics.text_attribute, Statistics.text_attribute_2,
                                 Statistics.int_attribute).filter(
            Statistics.type == "num_of_contracts_ministry").order_by(Statistics.text_attribute_2)

        for num_c in clist:
            mdict = ministeries[num_c.text_attribute]
            mdict["contract_count"] = num_c.int_attribute

        ilist = db.session.query(Statistics.type, Statistics.text_attribute, Statistics.text_attribute_2,
                                 Statistics.int_attribute).filter(
            Statistics.type == "num_of_invoices_ministry").order_by(Statistics.text_attribute_2)

        for num_i in ilist:
            mdict = ministeries[num_i.text_attribute]
            mdict["invoice_count"] = num_i.int_attribute

        wlist = db.session.query(Statistics.type, Statistics.text_attribute, Statistics.text_attribute_2,
                                 Statistics.int_attribute).filter(
            Statistics.type == "num_of_warnings_ministry").order_by(Statistics.text_attribute_2)

        for num_w in wlist:
            mdict = ministeries[num_w.text_attribute]
            mdict["warnings_count"] = num_w.int_attribute

        llist = db.session.query(Statistics.type, Statistics.text_attribute, Statistics.text_attribute_2,
                                 Statistics.int_attribute).filter(
            Statistics.type == "num_of_linked_ministry").order_by(Statistics.text_attribute_2)

        for num_l in llist:
            mdict = ministeries[num_l.text_attribute]
            mdict["linked_count"] = num_l.int_attribute

        for key, value in ministeries.items():
            reslist.append(value)
        res = jsonify(data=reslist)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_st.route('/invoices_ministry', methods=['GET'])
class InvoiceMinistryStats(Resource):
    def get(self):
        """
        Return invoice statistics per ministry.
        :return: Dist[str, List]
        """
        try:
            qlist = db.session.query(Statistics.text_attribute, Statistics.int_attribute).filter(Statistics.type == "num_invoices_per_ministry").order_by(Statistics.date_attribute)

            serializer = lambda i: {"ministry": i.text_attribute, "invoice_count": i.int_attribute}
            ministry_list = [serializer(i)["ministry"] for i in qlist]
            count_list = [serializer(i)["invoice_count"] for i in qlist]
        except OperationalError:
            ministry_list = []
            count_list = []

        res = jsonify(ministry=ministry_list, invoice_count=count_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_st.route('/contracts_ministry', methods=['GET'])
class ContractsMinistryStats(Resource):
    def get(self):
        """
        Return contracts statistics per ministry.
        :return: Dist[str, List]
        """
        try:
            qlist = db.session.query(Statistics.text_attribute, Statistics.int_attribute).filter(Statistics.type == "num_contracts_per_ministry").order_by(Statistics.date_attribute)

            serializer = lambda i: {"ministry": i.text_attribute, "contract_count": i.int_attribute}
            ministry_list = [serializer(i)["ministry"] for i in qlist]
            count_list = [serializer(i)["contract_count"] for i in qlist]
        except OperationalError:
            ministry_list = []
            count_list = []

        res = jsonify(ministry=ministry_list, contract_count=count_list)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_relations.route('/invoice/<int:invoice_id>', methods=['GET'])
class RelationsByInvoice(Resource):
    def get(self, invoice_id):
        """
        Return details about real relations and other relations linked to specific invoice.
        :return: Dist[str, List]
        """
        if invoice_id is None:
            relations = []
            final_relations = []
        else:
            try:
                qlist = db.session.query(PossibleRelation, Contract).join(Contract, Contract.contract_id == PossibleRelation.contract_id).filter(
                    PossibleRelation.invoice_id == invoice_id, PossibleRelation.contract_id is not None).order_by(PossibleRelation.contract_id)

                serializer = lambda r: {
                    "possible_relation_id": r[0].possible_relation_id,
                    "invoice_id": r[0].invoice_id,
                    "contract_id": r[0].contract_id,
                    "score": r[0].score,
                    "real": r[0].real,
                    "ministry_name": r[1].ministry_name,
                    "supplier_name": r[1].supplier_name,
                    "purpose": r[1].purpose,
                    "date_issue": r[1].date_agreed.strftime('%d.%m.%Y'),
                    "amount": max([i for i in [r[1].amount_with_dph, r[1].amount_without_dph] if i is not None], default=None)
                }
                relations = [serializer(i) for i in qlist if i[0].real is not True]
                final_relations = [serializer(i) for i in qlist if i[0].real is True]
            except OperationalError:
                final_relations = []
                relations = []

        res = jsonify(relations=relations, final_relations = final_relations)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res


@ns_relations.route('/contract/<int:contract_id>', methods=['GET'])
class RelationsByContract(Resource):
    def get(self, contract_id):
        """
        Return details about real relations and other relations linked to specific contract.
        :return: Dist[str, List]
        """
        if contract_id is None:
            relations = []
            final_relations = []
        else:
            try:
                qlist = db.session.query(PossibleRelation, Invoice).join(Invoice, Invoice.invoice_id == PossibleRelation.invoice_id).filter(
                    (PossibleRelation.contract_id == contract_id)).order_by(PossibleRelation.invoice_id)

                serializer = lambda r: {
                    "possible_relation_id": r[0].possible_relation_id,
                    "invoice_id": r[0].invoice_id,
                    "contract_id": r[0].contract_id,
                    "score": r[0].score,
                    "real": r[0].real,
                    "ministry_name": r[1].ministry_name,
                    "supplier_name": r[1].supplier_name,
                    "purpose": r[1].purpose,
                    "date_issue": r[1].date_issue.strftime('%d.%m.%Y'),
                    "amount": max([i for i in [r[1].amount_with_dph, r[1].amount_without_dph] if i is not None], default=None)

                }
                relations = [serializer(i) for i in qlist if i[0].real is not True]
                final_relations = [serializer(i) for i in qlist if i[0].real is True]
            except OperationalError:
                relations = []
                final_relations = []

        res = jsonify(relations=relations, final_relations=final_relations)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res

if __name__ == '__main__':
    parser = ConfigParser()
    parser.read("configuration.ini")
    host = parser['Flask']['host']
    port = parser['Flask'].getint('port')
    debug = parser['Flask'].getboolean('debug')
    app.run(host=host, port=port, debug=debug)
