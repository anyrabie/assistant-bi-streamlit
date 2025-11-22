import ollama
import sqlite3 as sql
import pandas as pd
import json

class AssistantBI:
    def __init__(self, db_path='./DataSet/dw_ventes.db', model='llama3.2:3b'):
        self.db_path = db_path
        self.model = model
        self.conn = sql.connect(db_path)
        
        self.schema = self._get_schema()
        
    def _get_schema(self):
        query = """
        SELECT name FROM sqlite_master WHERE type = 'table'
        """
        tables = pd.read_sql_query(query, self.conn)
        
        schema_info = {}
        for table in tables['name']:
            query = f"PRAGMA table_info({table})"
            columns = pd.read_sql_query(query, self.conn)
            schema_info[table] = columns['name'].tolist()
            
        return schema_info
    
    def generer_sql(self, question):
        
        schema_text = "\n".join([
            f"Table '{table}':{','.join(cols)}"
            for table, cols in self.schema.items()
        ])
        
        prompt = f"""Tu es un expert en SQL et analyse de donnees.
Schema de la base de donnees :
{schema_text}

Question utilisateur : {question}
Instructions :
1. Genere UNIQUEMENT une requete SQL valide
2. Utilise les bonnes tables selon la question
3. Ajoute ORDER BY et LIMIT si pertinent
4. Reponds SEULEMENT avec le SQL, sans texte additionnel
 
 Requete SQL :"""
 
        reponse = ollama.chat(
            model=self.model,
            messages = [{'role': 'user', 'content': prompt}]
            
        )
        
        sql = reponse['message']['content'].strip()
        
        sql = sql.replace("```sql", "").replace("```", "").strip()
        
        return sql
    
    def executer_requete(self, sql):
        try:
            resultat = pd.read_sql_query(sql, self.conn)
            return resultat, None
        except Exception as e:
            return None, str(e)
        
    def generer_reponse(self, question, resultats):
        if resultats is None or resultats.empty:
            return "Aucune donne trouve pour cette question."
        data_summary = resultats.head(10).to_dict(orient='records')
        
        prompt = f"""Tu es un analyste BI professionnel.
 
 Question initiale : {question}

 Resultats de l’analyse :
 {json.dumps(data_summary, indent=2)}
Instructions :
1. Reponds en francais de maniere claire et professionnelle
2. Mentionne les chiffres cles
3. Ajoute un insight si pertinent
4. Sois concis (3-4 phrases maximum)

 Reponse :"""
 
        reponse = ollama.chat(
            model=self.model,
            messages = [{'role': 'user', 'content':prompt}]
            
        )
        return reponse['message']['content']
    
    def interroger(self, question):

        print(f"\n[QUESTION] {question}")

        # 1) Génération SQL
        sql = self.generer_sql(question)
        print(f"\n[SQL GENERE]\n{sql}")

        # 2) Exécution SQL sécurisée
        resultats, erreur = self.executer_requete(sql)

        if erreur:
            print("[ERREUR SQL] ", erreur)
            return f"Erreur dans la requête SQL générée :\n{erreur}\n\nSQL utilisé :\n{sql}", None

        print(f"\n[RESULTATS] {len(resultats)} lignes")

        # 3) Si aucun résultat
        if not resultats:
            return "La requête n’a retourné aucun résultat.", []

        # 4) Génération réponse
        try:
            reponse = self.generer_reponse(question, resultats)
        except Exception as e:
            return f"Erreur lors de la génération de la réponse IA : {e}", resultats

        return reponse, resultats

        
if __name__=='__main__':
    assistant = AssistantBI()
    
    questions = [
    "Quelle categorie genere le plus de profit ?",
    "Quelles sont les ventes totales par region ?",
    "Quel est le produit le plus vendu ?"
    ]
    
    for q in questions:
        reponse, data = assistant.interroger(q)
        print(f"\n[REPONSE]\n{reponse}\n")
        print("-" * 60)
        