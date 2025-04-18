import streamlit as st
from database import add_record

def create_registration_form():
    """Create and handle the protocol registration form"""
    with st.form(key="Registration_Form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            rota = st.text_input('Número da Rota:')
            motorista = st.text_input('Nome do Motorista:')
            transportadora = st.text_input('Nome da Transportadora:')
            data_registro = st.date_input('Data:')
        
        with col2:
            pedido = st.text_input('Número do Pedido:')
            remessa = st.text_input('Número da Remessa:')
            nota_fiscal = st.text_input('Número da Nota Fiscal:')
            motivo = st.text_area('Motivo da Devolução:', height=100)
        
        submit = st.form_submit_button(label='Registrar Protocolo')

        if submit:
            # Validate required fields
            if not rota or not motorista or not transportadora:
                st.error('Os campos Rota, Motorista e Transportadora são obrigatórios.')
                return
            
            # Add record to database
            record_id = add_record(
                rota, motorista, transportadora, 
                pedido, remessa, nota_fiscal, 
                motivo, data_registro
            )
            
            if record_id:
                st.success(f'Devolução cadastrada com sucesso. ID do Registro: {record_id}')
                
                # Display a summary of the registration
                st.markdown("### Resumo do Registro")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Rota:** {rota}")
                    st.write(f"**Motorista:** {motorista}")
                    st.write(f"**Transportadora:** {transportadora}")
                    st.write(f"**Data:** {data_registro}")
                
                with col2:
                    st.write(f"**Pedido:** {pedido}")
                    st.write(f"**Remessa:** {remessa}")
                    st.write(f"**Nota Fiscal:** {nota_fiscal}")