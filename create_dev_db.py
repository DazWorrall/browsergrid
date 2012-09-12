#!/usr/bin/env python
from browsergrid.app import init_db, create_app
a = create_app()
init_db(a)
print 'Done!'
