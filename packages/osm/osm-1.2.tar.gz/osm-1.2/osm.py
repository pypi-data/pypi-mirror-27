#!/usr/bin/python

"""
Optimal Stellar Models (OSM)

Copyright (c) 2012 R. Samadi (LESIA - Observatoire de Paris)

This is a free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this code.  If not, see <http://www.gnu.org/licenses/>.
"""
 
__version__ = "1.2"

import os,sys,traceback
import getopt
from osmlib import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def search_guess():
    
    ans = ''
    gridname = 'grid'
    path = '/data/samadi/models/grids/mlt/cestam/HR/m00/'
    ans = (raw_input("The grid name: " + gridname))
    if(ans != ''):
        gridname = ans
    ans = (raw_input("Full path: " + path))
    if(ans != ''):
        path = ans
    while( ans != 'q'):
        print "Type 'q' to quit"
        ans = (raw_input("log g: ")).lower()
        if(ans != 'q'):
            logg = float(ans)
            ans = (raw_input("Teff: ")).lower()
            if(ans != 'q'):
                teff = float(ans)
                search_model_in_grid(logg,teff,gridname,path,dteff=50., dlogg=0.1,old=False)           
    

def main():

    def copyright():

        print    "\n\
        Optimal Stellar Models (OSM)\n\
        \n\
        Copyright (c) 2012 R. Samadi (LESIA - Observatoire de Paris)\n\
        \n\
        This is a free software: you can redistribute it and/or modify\n\
        it under the terms of the GNU General Public License as published by\n\
        the Free Software Foundation, either version 3 of the License, or\n\
        (at your option) any later version.\n\
        \n\
        This software is distributed in the hope that it will be useful,\n\
        but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
        GNU General Public License for more details.\n\
        You should have received a copy of the GNU General Public License\n\
        along with this code.  If not, see <http://www.gnu.org/licenses/>.\n"


    def usage():
        print "This is OSM version: " + __version__
        print "usage : osm [-e] name.xml "
        print "usage : osm -G"
        print "usage : osm -v"

        print "Option:"
        print "-e <address> : send an email to <address> after completion"
        print "-G : search guess parameters in a grid"
        print "-v : print code version and exit"

    if(len(sys.argv)<2):
        copyright()
        usage()
        sys.exit(2)
    try:
        opts,args = getopt.getopt(sys.argv[1:],"he:G:v")

    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
        
    email = ''
    guess_flag = False
    for o, a in opts:
        if o == "-h" :
            usage()
            sys.exit(1)
        elif o == "-v":
            print __version__
            sys.exit(1)
        elif o == "-e":
            email = a.strip()
        elif o == "-G" :
            guess_flag = True
        else:
            print "unhandled option %s" % (o)
            sys.exit(1)
             
    print "This is OSM version: " + __version__

    if(guess_flag):
        search_guess()
        sys.exit(1)

    nargs = len(args)
    if nargs > 1 :
        print "too many arguments"
        usage()
        sys.exit()

    if nargs < 1 :
        print "missing arguments"
        usage()
        sys.exit()


    name =  re.sub('\.xml','',os.path.basename(args[0]))

    if(email != ''):
        sys.stdout = open(name+'.log', 'w')

    copyright()

    cwd = os.getcwd()

    try:
    	parameters,targets,settings,seismic_constraints = osminit(name)
    except OSMError as e:
        results=  traceback.format_exc()
        raise
    except:
	results  = traceback.format_exc()  # ("Unexpected error: %s") % (sys.exc_info()[0])
        raise
    
    if(email != ''):
        print ''
        print 'Running OSM, results will be sent to ' + email
        sys.stdout.flush()
         # Create the container (outer) email message.
        msg = MIMEMultipart()
        s = ('OSM: starting %s (job PID= %d)')  % ( name ,  os.getpid()  )
        msg['Subject'] = s
        msg['From'] = email
        msg['To'] = email
        msg.preamble = 'OSM'
        msg.attach( MIMEText(s))
        
        f = name+'.log'
        part = MIMEBase('text', "plain")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)       

        f = name+'.xml'
        part = MIMEBase('text', "xml")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_quopri(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
        
        f = name+'.don'
        part = MIMEBase('text', "plain")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)       

        # Send the email via our own SMTP server.
        try:
            s = smtplib.SMTP('localhost')
        except: # Send the email via smtp.obspm.fr
            try:
                s = smtplib.SMTP('smtp.obspm.fr')
            except:
                sys.stdout.close()
                sys.stdout = sys.__stdout__
                print 'an error occurs while sending the email'
                raise

        try:
            s.sendmail(email, email, msg.as_string())
            s.quit()
        except:
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            print 'an error occurs while sending the email'
            raise

    if(email != ''):
        sys.stderr = open(name+'.err', 'w')
       
    try:
    	results = osmrun(name,parameters,targets,settings,seismic_constraints)
    except OSMError as e:
        results=  traceback.format_exc()
        if(email == ''):
            print results
            raise
    except:
	results  = traceback.format_exc()  # ("Unexpected error: %s") % (sys.exc_info()[0])
        if(email == ''):
            print results
            raise

    os.chdir(cwd)
    sys.stdout.flush()  
    sys.stderr.flush()
    if(email != ''):
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = 'OSM: results for  ' + name
        msg['From'] = email
        msg['To'] = email
        msg.preamble = 'OSM'

        msg.attach( MIMEText(results ))

        f = name+'.log'
        part = MIMEBase('text', "plain")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)       

        # Send the email via our own SMTP server.
        try:
            s = smtplib.SMTP('localhost')
        except: # Send the email via smtp.obspm.fr
            try:
                s = smtplib.SMTP('smtp.obspm.fr')
            except:
                raise
        try:
            s.sendmail(email, email, msg.as_string())
            s.quit()
        except:
            raise
        

if __name__ == "__main__":
    main()

