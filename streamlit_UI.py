import streamlit as st 

st.set_page_config(
    page_title='Assistant BI Conversationnel',
    page_icon='',
    layout='wide'
)

@st.cache_resource
def load_assistant():
    return "rabie"

def main():
    st.title("Assistant BI Conversationnel")
    assistant = load_assistant()
    st.markdown("*Posez vos questions en langage naturel*")
    #st.write("Assistant chargé:", assistant)
    question = st.text_input(
        'Votre question :',
        placeholder="Ex: Quelle region a le meilleur chiffre d'affaires ?"
    )
    
    if st.button('Analyser', type='primary'):
        if question:
            with st.spinner('Analyse en cours ...'):
                
                st.success('Reponse')
                st.write('reponse')
        else:
            st.warning('Veuillez saisir une question')

    st.sidebar.header('Questions exemples')
    exemples = [
        'Top 5 des produits les plus rentables',
        'Evolution des ventes par trimestre',
        'Quelle categorie a la marge la plus faible ?'
    ]
    
    for ex in exemples:
        if st.sidebar.button(ex):
            st.session_state.question = ex
if __name__ == "__main__":
    main()
