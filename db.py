import appauth

psdbname = 'opsView'
psdbserver = 'psqlServerName.domain.com'
psdbuser = appauth.getpsqluser()
psdbpass = appauth.getpsqlsecrect()
dbsslmode = 'require'