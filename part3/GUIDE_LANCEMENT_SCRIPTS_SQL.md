# 🚀 Guide de Lancement des Scripts SQL

**Projet** : HBnB Evolution - Part 3
**Date** : 2025-11-08

---

## 📋 Pré-requis

### **1. Vérifier que MySQL est installé**

```bash
# Vérifier la version de MySQL
mysql --version

# Devrait afficher quelque chose comme :
# mysql  Ver 8.0.35 for macos13.3 on arm64 (Homebrew)
```

**Si MySQL n'est pas installé** :

**macOS** :
```bash
brew install mysql
brew services start mysql
```

**Ubuntu/Debian** :
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
```

---

### **2. Configurer le mot de passe root MySQL**

```bash
# Se connecter à MySQL (la première fois, pas de mot de passe)
mysql -u root

# OU si mot de passe déjà configuré
mysql -u root -p
```

**Si vous n'avez pas de mot de passe root** :
```sql
-- Dans MySQL :
ALTER USER 'root'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
FLUSH PRIVILEGES;
EXIT;
```

---

## 🎯 MÉTHODE 1 : Exécution depuis le Terminal (Recommandé)

### **Étape 1 : Aller dans le dossier part3**

```bash
# Depuis n'importe où
cd /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb/part3

# Vérifier que vous êtes au bon endroit
ls -la
# Vous devriez voir : sql_scripts_task9.sql, sql_tests_validation.sql

# Vérifier le chemin complet
pwd
# /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb/part3
```

---

### **Étape 2 : Créer la base de données**

**Option A : Exécution directe depuis le terminal**
```bash
# Exécuter le script de création
mysql -u root -p < sql_scripts_task9.sql

# MySQL va demander votre mot de passe
# Enter password: [tapez votre mot de passe]

# Le script va s'exécuter complètement
# Aucune sortie = succès
```

**Option B : Avec des messages de progression**
```bash
# Exécuter avec affichage des messages
mysql -u root -p -v < sql_scripts_task9.sql

# L'option -v (verbose) affiche les commandes exécutées
```

**Option C : Rediriger la sortie dans un fichier log**
```bash
# Sauvegarder les logs dans un fichier
mysql -u root -p -v < sql_scripts_task9.sql > creation_log.txt 2>&1

# Voir le contenu du log
cat creation_log.txt
```

---

### **Étape 3 : Vérifier la création**

```bash
# Se connecter à la base créée
mysql -u root -p hbnb_prod

# Vous devriez voir le prompt MySQL :
# mysql>
```

**Dans MySQL**, exécutez :
```sql
-- Vérifier les tables créées
SHOW TABLES;

-- Devrait afficher :
-- +---------------------+
-- | Tables_in_hbnb_prod |
-- +---------------------+
-- | amenities           |
-- | place_amenity       |
-- | places              |
-- | reviews             |
-- | users               |
-- +---------------------+

-- Vérifier qu'il y a des données
SELECT * FROM users;
SELECT * FROM amenities;

-- Vérifier les contraintes
SHOW CREATE TABLE users\G

-- Quitter
EXIT;
```

---

### **Étape 4 : Exécuter les tests de validation**

```bash
# Depuis le dossier part3
mysql -u root -p hbnb_prod < sql_tests_validation.sql

# ⚠️ IMPORTANT : Ce script va générer des ERREURS VOLONTAIRES
# C'est NORMAL ! Les tests vérifient que les validations fonctionnent

# Exemple de sortie attendue :
# ERROR 3819 (HY000) at line 25: Check constraint 'chk_email_format' is violated.
# ✅ C'est BON ! Ça veut dire que la validation fonctionne
```

**Pour voir tous les résultats des tests** :
```bash
# Exécuter avec verbose et sauvegarder
mysql -u root -p hbnb_prod -v < sql_tests_validation.sql > tests_log.txt 2>&1

# Voir le log
cat tests_log.txt

# Ou avec less (navigation facile)
less tests_log.txt
# (Appuyez sur 'q' pour quitter)
```

---

## 🎯 MÉTHODE 2 : Exécution depuis MySQL Interactive

### **Étape 1 : Se connecter à MySQL**

```bash
mysql -u root -p

# Enter password: [votre mot de passe]
```

---

### **Étape 2 : Exécuter le script de création**

**Dans MySQL** :
```sql
-- Utiliser la commande SOURCE
SOURCE /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb/part3/sql_scripts_task9.sql;

-- MySQL va exécuter tout le script
-- Vous verrez défiler les commandes

-- Vérifier la base créée
SHOW DATABASES;

-- Utiliser la base
USE hbnb_prod;

-- Vérifier les tables
SHOW TABLES;
```

---

### **Étape 3 : Exécuter les tests**

**Dans MySQL** :
```sql
-- Vous devez être dans la base hbnb_prod
USE hbnb_prod;

-- Exécuter les tests
SOURCE /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb/part3/sql_tests_validation.sql;

-- ⚠️ Vous allez voir des ERREURS, c'est NORMAL
-- Exemple :
-- ERROR 3819 (HY000): Check constraint 'chk_email_format' is violated.
```

---

## 🎯 MÉTHODE 3 : Exécution avec MySQL Workbench (GUI)

### **Étape 1 : Ouvrir MySQL Workbench**

1. Lancer MySQL Workbench
2. Se connecter à votre serveur MySQL local
3. Cliquer sur "File" → "Open SQL Script"
4. Sélectionner `sql_scripts_task9.sql`

---

### **Étape 2 : Exécuter le script**

1. Le script s'ouvre dans l'éditeur
2. Cliquer sur l'icône ⚡ "Execute" (ou Ctrl+Shift+Enter)
3. Attendre la fin de l'exécution
4. Vérifier dans le panneau "Schemas" à gauche : `hbnb_prod` devrait apparaître

---

### **Étape 3 : Exécuter les tests**

1. Ouvrir `sql_tests_validation.sql`
2. Sélectionner la base `hbnb_prod` dans la dropdown en haut
3. Cliquer sur ⚡ "Execute"
4. Voir les résultats dans l'onglet "Output"

---

## ✅ Vérifications Après Exécution

### **Test 1 : Vérifier que la base existe**

```bash
mysql -u root -p -e "SHOW DATABASES LIKE 'hbnb_prod';"

# Devrait afficher :
# +----------------------+
# | Database (hbnb_prod) |
# +----------------------+
# | hbnb_prod            |
# +----------------------+
```

---

### **Test 2 : Compter les tables**

```bash
mysql -u root -p hbnb_prod -e "SHOW TABLES;"

# Devrait afficher 5 tables
```

---

### **Test 3 : Vérifier les données initiales**

```bash
# Compter les users
mysql -u root -p hbnb_prod -e "SELECT COUNT(*) FROM users;"

# Devrait afficher au moins 1 (l'admin)

# Compter les amenities
mysql -u root -p hbnb_prod -e "SELECT COUNT(*) FROM amenities;"

# Devrait afficher 4 (WiFi, Parking, Pool, Air Conditioning)
```

---

### **Test 4 : Vérifier les contraintes**

```bash
mysql -u root -p hbnb_prod -e "
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'hbnb_prod'
ORDER BY TABLE_NAME;
"

# Devrait lister toutes les contraintes (PK, FK, UK, CHECK)
```

---

### **Test 5 : Vérifier le trigger**

```bash
mysql -u root -p hbnb_prod -e "SHOW TRIGGERS\G"

# Devrait afficher :
# Trigger: trg_prevent_self_review
# Timing: BEFORE
# Event: INSERT
```

---

### **Test 6 : Vérifier les vues**

```bash
mysql -u root -p hbnb_prod -e "
SELECT TABLE_NAME
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = 'hbnb_prod';
"

# Devrait afficher :
# +--------------------+
# | TABLE_NAME         |
# +--------------------+
# | v_place_statistics |
# | v_user_statistics  |
# +--------------------+
```

---

## 🐛 Résolution de Problèmes

### **Problème 1 : "ERROR 1045 (28000): Access denied"**

**Cause** : Mauvais mot de passe ou user

**Solution** :
```bash
# Vérifier l'utilisateur
mysql -u root -p

# Si ça ne marche pas, réinitialiser le mot de passe
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nouveau_mot_de_passe';
FLUSH PRIVILEGES;
EXIT;
```

---

### **Problème 2 : "ERROR 1007 (HY000): Can't create database 'hbnb_prod'; database exists"**

**Cause** : La base existe déjà

**Solution** :
```bash
# Option 1 : Supprimer l'ancienne base (⚠️ ATTENTION : supprime toutes les données!)
mysql -u root -p -e "DROP DATABASE IF EXISTS hbnb_prod;"

# Puis relancer le script
mysql -u root -p < sql_scripts_task9.sql

# Option 2 : Renommer la base existante
mysql -u root -p -e "
CREATE DATABASE hbnb_prod_backup;
-- Ensuite exporter/importer les tables si besoin
"
```

---

### **Problème 3 : "ERROR 1064 (42000): You have an error in your SQL syntax"**

**Cause** : Version MySQL trop ancienne (< 8.0.16) ou caractères spéciaux

**Solution** :
```bash
# Vérifier la version
mysql --version

# Si version < 8.0.16, les CHECK constraints ne sont pas supportés
# Les erreurs seront ignorées mais les contraintes ne s'appliqueront pas
```

---

### **Problème 4 : "ERROR 2002 (HY000): Can't connect to local MySQL server"**

**Cause** : MySQL n'est pas démarré

**Solution** :
```bash
# macOS (Homebrew)
brew services start mysql

# Ubuntu/Debian
sudo systemctl start mysql
sudo systemctl status mysql

# Vérifier que MySQL écoute
sudo lsof -i :3306
```

---

### **Problème 5 : "ERROR 1217 (23000): Cannot delete or update a parent row"**

**Cause** : Tentative de suppression avec foreign keys actives

**Solution** :
```sql
-- Désactiver temporairement les foreign key checks
SET FOREIGN_KEY_CHECKS = 0;

-- Supprimer la base
DROP DATABASE IF EXISTS hbnb_prod;

-- Réactiver
SET FOREIGN_KEY_CHECKS = 1;
```

---

## 📊 Scripts de Maintenance

### **Sauvegarder la base**

```bash
# Dump complet de la base
mysqldump -u root -p hbnb_prod > hbnb_prod_backup_$(date +%Y%m%d).sql

# Vérifier le fichier créé
ls -lh hbnb_prod_backup_*.sql
```

---

### **Restaurer depuis un backup**

```bash
# Créer une nouvelle base (si nécessaire)
mysql -u root -p -e "CREATE DATABASE hbnb_prod_restore;"

# Restaurer
mysql -u root -p hbnb_prod_restore < hbnb_prod_backup_20251108.sql
```

---

### **Voir les logs MySQL**

```bash
# macOS (Homebrew)
tail -f /usr/local/var/mysql/$(hostname).err

# Ubuntu/Debian
sudo tail -f /var/log/mysql/error.log
```

---

### **Réinitialiser complètement**

```bash
# 1. Supprimer la base
mysql -u root -p -e "DROP DATABASE IF EXISTS hbnb_prod;"

# 2. Relancer le script de création
mysql -u root -p < sql_scripts_task9.sql

# 3. Vérifier
mysql -u root -p hbnb_prod -e "SHOW TABLES;"
```

---

## 🎯 Commandes Rapides (Cheat Sheet)

```bash
# Créer la base
mysql -u root -p < sql_scripts_task9.sql

# Tester les validations
mysql -u root -p hbnb_prod < sql_tests_validation.sql

# Se connecter à la base
mysql -u root -p hbnb_prod

# Lister les tables
mysql -u root -p hbnb_prod -e "SHOW TABLES;"

# Voir les users
mysql -u root -p hbnb_prod -e "SELECT * FROM users;"

# Voir les amenities
mysql -u root -p hbnb_prod -e "SELECT * FROM amenities;"

# Voir les statistiques
mysql -u root -p hbnb_prod -e "SELECT * FROM v_user_statistics;"

# Backup
mysqldump -u root -p hbnb_prod > backup.sql

# Restore
mysql -u root -p hbnb_prod < backup.sql

# Supprimer la base
mysql -u root -p -e "DROP DATABASE hbnb_prod;"
```

---

## 📚 Ressources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Command-Line Tool](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)
- [mysqldump Documentation](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)

---

## ✅ Checklist de Vérification Finale

Après avoir lancé les scripts, vérifiez :

- [ ] La base `hbnb_prod` existe
- [ ] 5 tables créées (users, places, reviews, amenities, place_amenity)
- [ ] Au moins 1 user dans la table users (admin@hbnb.com)
- [ ] 4 amenities dans la table amenities
- [ ] Le trigger `trg_prevent_self_review` existe
- [ ] Les 2 vues existent (v_user_statistics, v_place_statistics)
- [ ] Les contraintes CHECK fonctionnent (tests génèrent des erreurs)
- [ ] Les foreign keys fonctionnent (cascade delete)

**Commande de vérification complète** :
```bash
mysql -u root -p hbnb_prod << 'EOF'
SELECT 'Tables:' AS check_type, COUNT(*) AS count FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'hbnb_prod'
UNION ALL
SELECT 'Users:', COUNT(*) FROM users
UNION ALL
SELECT 'Amenities:', COUNT(*) FROM amenities
UNION ALL
SELECT 'Triggers:', COUNT(*) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = 'hbnb_prod'
UNION ALL
SELECT 'Views:', COUNT(*) FROM information_schema.VIEWS WHERE TABLE_SCHEMA = 'hbnb_prod';
EOF
```

**Résultat attendu** :
```
+------------+-------+
| check_type | count |
+------------+-------+
| Tables:    |     5 |
| Users:     |     2 |
| Amenities: |     4 |
| Triggers:  |     1 |
| Views:     |     2 |
+------------+-------+
```

---

**Créé le** : 2025-11-08
**Par** : Thomas
**Projet** : HBnB Evolution - Part 3

✅ **Vos scripts SQL sont maintenant prêts à être exécutés !**
