#------------------------------------------------------------------------------------------------------------------------------------------//
#------------------------------------------------------------------------------------------------------------------------------------------//
#---------------------- Nome: LM PreCadastr isCPFinDB.py
#------------------- Doctype: LM PreCadastro
#----------------- Descricao: Verifica se um CPF já existe em Customer
#------------------ Contexto: Pré Cadastro de um usuário na etapa de Inscrições
#---------------------- Data: 16/05/2024
#--------------------- Autor: Eduardo Kuniyoshi (EK)
#--- Histórico de alterações:
#----------------------------  1.0 - EK - 19/04/2024 - Liberação da versão para o processo de inscrição 2o. Sem/2024
#----------------------------  2.0 - EK - 18/05/2024 - Otimização
#------------------------------------------------------------------------------------------------------------------------------------------//
#------------------------------------------------------------------------------------------------------------------------------------------//

def isCPFinDB(args):
    try:
        dict_doc = json.loads(args.doc)

        if dict_doc["name"][:4] == "new-" : 
            NewDoc = frappe.new_doc("LM PreCadastro")
            NewDoc.set("status",                "Cadastro Conferido")   
            NewDoc.set("cpf",                   dict_doc["cpf"])
            NewDoc.set("ifchecked",             1)
            if frappe.db.exists("Customer", {"tax_id": dict_doc["cpf"]}):
                # Definir o valor do campo no novo documento
                NewDoc.set("cpf_ok",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cpf_validado"))
                NewDoc.set("cpf_provisorio",        frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cpf_provisório"))
                NewDoc.set("full_name",             frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "customer_name"))
                NewDoc.set("usuario",               frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "customer_name"))
                NewDoc.set("rg",                    frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "rg"))
                NewDoc.set("ifexist",               1)
                NewDoc.set("date_of_birth",         frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "data_de_nascimento"))
                NewDoc.set("idade",                 frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "idade"))
                NewDoc.set("gender",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "gender"))
                NewDoc.set("nationality",           frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "nacionalidade"))
                NewDoc.set("escolaridade",          frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "escolaridade"))
                NewDoc.set("situacao_ocupacional",  frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "situacao_laboral"))
                NewDoc.set("student_mobile_number", frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "celular"))
                NewDoc.set("obs_cel",               frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "observações_recado"))
                NewDoc.set("student_email_id",      frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "email"))
                NewDoc.set("email_provisorio",      frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "email_provisorio"))
                NewDoc.set("email_confirmado",      frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "email_confirmado"))
                NewDoc.set("cep",                   frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cep"))
                NewDoc.set("endereço",              frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "endereço"))
                NewDoc.set("bairro",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "bairro"))
                NewDoc.set("número",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "número"))
                NewDoc.set("cidade",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cidade"))
                NewDoc.set("complemento",           frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "complemento"))
                NewDoc.set("estado",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "estado"))
                NewDoc.set("image",                 frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "image"))
                
                if frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_mae") :
                    NewDoc.set("nome_mãe",              frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_mae"))
                else : NewDoc.set("nome_mãe",           "*** NÃO INFORMADO")
                if frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_pai") :
                    NewDoc.set("nome_pai",              frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_pai"))
                else : NewDoc.set("nome_pai",           "*** NÃO INFORMADO")
                if frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_resp") :
                    NewDoc.set("nome_resp",             frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_resp"))
                else : NewDoc.set("nome_resp",           "*** NÃO INFORMADO")

                # Salvar o novo documento
                NewDoc.insert()
                NewUrl = frappe.utils.get_url_to_form('LM PreCadastro', NewDoc.name)
                html_content = f'''
                <div>
                    <b>CPF <a href="{NewUrl}" target="_blank"> {dict_doc["cpf"]}</a></b> localizado no Cadastro Lar Meimei. <br>
                    <b>Clique no link <a href="{NewUrl}" target="_blank"> {dict_doc["cpf"]}</a></b> para carregar os dados existentes para confirmação e eventual correção ou complementação.
                </div>
                '''
                # exibe a mensagem com o link criado. (nao consegui abrir diretamente)
                frappe.msgprint(html_content)
                
                #frappe.set_route('Form', 'LM PreCadastro', NewDoc.name)
            else : # o CPF não existe
                NewDoc.set("cpf_ok",                dict_doc["cpf_ok"])
                NewDoc.set("cpf_provisorio",        dict_doc["cpf_provisorio"])
                if (dict_doc["full_name"]) :
                    NewDoc.set("full_name",             dict_doc["full_name"])
                else : 
                    NewDoc.set("full_name",             "DIGITE O NOME")
                NewDoc.set("usuario",               "")
                NewDoc.set("rg",                    "")
                NewDoc.set("ifexist",               0)
                NewDoc.set("date_of_birth",         frappe.utils.today())
                NewDoc.set("idade",                 dict_doc["idade"])
                NewDoc.set("gender",                "")
                NewDoc.set("nationality",           dict_doc["nationality"])
                NewDoc.set("escolaridade",          dict_doc["escolaridade"])
                NewDoc.set("situacao_ocupacional",  dict_doc["situacao_ocupacional"])
                NewDoc.set("student_mobile_number", dict_doc["student_mobile_number"])
                NewDoc.set("obs_cel",               "")
                NewDoc.set("student_email_id",      str(dict_doc["cpf_ok"])+"@larmeimei.org")
                NewDoc.set("email_provisorio",      dict_doc["email_provisorio"])
                NewDoc.set("email_confirmado",      dict_doc["email_confirmado"])
                NewDoc.set("cep",                   dict_doc["cep"])
                NewDoc.set("endereço",              dict_doc["endereço"])
                NewDoc.set("bairro",                dict_doc["bairro"])
                NewDoc.set("número",                "")
                NewDoc.set("cidade",                dict_doc["cidade"])
                NewDoc.set("complemento",           "")
                NewDoc.set("estado",                dict_doc["estado"])
                NewDoc.set("image",                 "")
                NewDoc.set("nome_mãe",              dict_doc["nome_mãe"])
                NewDoc.set("nome_pai",              dict_doc["nome_pai"])
                NewDoc.set("nome_resp",             dict_doc["nome_resp"])

                # Salvar o novo documento
                NewDoc.insert()
                NewUrl = frappe.utils.get_url_to_form('LM PreCadastro', NewDoc.name)
                html_content = f'''
                <div>
                    <b>CPF <a href="{NewUrl}" target="_blank"> {dict_doc["cpf"]}</a></b> NÃO localizado no Cadastro Lar Meimei.<br>
                    Clique no link para continuar a digitação dos dados: <b><a href="{NewUrl}" target="_blank"> {dict_doc["cpf"]}</a></b>.
                </div>
                '''
                # exibe a mensagem com o link criado. (nao consegui abrir diretamente)
                frappe.msgprint(html_content)

        else :  # o registro não é novo
            doc = frappe.get_doc("LM PreCadastro", dict_doc["name"])    
            doc.set("ifchecked",             1)
            doc.update({"status"    : "Cadastro Conferido"})
            if frappe.db.exists("Customer", {"tax_id": dict_doc["cpf"]}):
                doc.set("cpf",                   dict_doc["cpf"])
                doc.set("cpf_ok",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cpf_validado"))
                doc.set("cpf_provisorio",        frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cpf_provisório"))
                #doc.set("full_name",             frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "customer_name"))
                doc.set("usuario",               frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "customer_name"))
                doc.set("rg",                    frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "rg"))
                doc.set("ifexist",               1)
                doc.set("date_of_birth",         frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "data_de_nascimento"))
                doc.set("idade",                 frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "idade"))
                doc.set("gender",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "gender"))
                doc.set("nationality",           frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "nacionalidade"))
                doc.set("escolaridade",          frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "escolaridade"))
                doc.set("situacao_ocupacional",  frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "situacao_laboral"))
                doc.set("student_mobile_number", frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "celular"))
                doc.set("obs_cel",               frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "observações_recado"))
                doc.set("student_email_id",      frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "email"))
                doc.set("email_provisorio",      frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "email_provisorio"))
                doc.set("email_confirmado",      frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "email_confirmado"))
                doc.set("cep",                   frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cep"))
                doc.set("endereço",              frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "endereço"))
                doc.set("bairro",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "bairro"))
                doc.set("número",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "número"))
                doc.set("cidade",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cidade"))
                doc.set("complemento",           frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "complemento"))
                doc.set("estado",                frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "estado"))
                doc.set("image",                 frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "image"))

                if frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_mae") :
                    doc.set("nome_mãe",              frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_mae"))
                else : doc.set("nome_mãe",           "*** NÃO INFORMADO")
                if frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_pai") :
                    doc.set("nome_pai",              frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_pai"))
                else : doc.set("nome_pai",           "*** NÃO INFORMADO")
                if frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_resp") :
                    doc.set("nome_resp",             frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "cr_nome_resp"))
                else : doc.set("nome_resp",           "*** NÃO INFORMADO")
                
                if doc.full_name != frappe.db.get_value("Customer", {"tax_id": dict_doc["cpf"]}, "customer_name") :
                    frappe.msgprint(f'*** ATENÇÃO! NOME COMPLETO diferente do nome cadastrado. É necessário verificar e reiniciar o cadastramento.')
                    doc.update({"ifchecked" : 0})
                    doc.update({"status"    : "Pré Cadastro"})
               
            else : # o CPF não existe na base
                frappe.msgprint(f'CPF {dict_doc["cpf"]} NÃO localizado no Cadastro Lar Meimei. Finalize o preenchimento do formulário.')
                doc.set("ifexist",               0)
            
            doc.save()

    except Exception as e:
      # Handle the error
      frappe.msgprint(f"*** isCPFinDB: {e} ")
      # Log the error or display a custom message to the user

isCPFinDB(args)
