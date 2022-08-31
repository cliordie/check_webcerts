import appauth

psdbname = 'opsView'
psdbserver = 'iuhlopsvap01.chp.clarian.org'
psdbuser = appauth.getpsqluser()
psdbpass = appauth.getpsqlsecrect()
dbsslmode = 'require'