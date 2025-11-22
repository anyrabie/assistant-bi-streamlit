# Projet gen_IA_mini_projet

Ce dépôt contient un environnement virtuel Python local `.venv`.

## Activation (PowerShell — recommandé)
```powershell
Set-Location -Path 'c:\Users\HP\Desktop\ING4-IA\S7\BI\Expose_mini_projet\gen_IA_mini_projet'
.\.venv\Scripts\Activate.ps1
```

Si l'exécution est bloquée, exécutez (optionnel, peut demander des droits élevés):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Activation (cmd.exe)
```
cd /d c:\Users\HP\Desktop\ING4-IA\S7\BI\Expose_mini_projet\gen_IA_mini_projet
.venv\Scripts\activate.bat
```

## Activation (Git Bash / WSL)
```
cd 'c:/Users/HP/Desktop/ING4-IA/S7/BI/Expose_mini_projet/gen_IA_mini_projet'
source .venv/Scripts/activate
```

## Utiliser Python sans activer
```
.venv\Scripts\python script.py
```

## Installer dépendances
- Ajoutez vos dépendances dans `requirements.txt` puis exécutez:
```powershell
pip install -r requirements.txt
```

## Vérification
- Vérifier la version Python du venv:
```powershell
.venv\Scripts\python -V
```

---
Fait: venv créé et Python détecté: `Python 3.12.4`.
