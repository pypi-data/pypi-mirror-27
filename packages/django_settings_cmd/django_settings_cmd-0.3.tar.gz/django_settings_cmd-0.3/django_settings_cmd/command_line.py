import sys,os,re

def find_settings():
    for root, dirs, files in os.walk("."):
        if "settings.py" in files:
            return os.path.join(root, "settings.py")
    return None        

def enable_app():
    if( len(sys.argv) != 2 ):
        print("Expecting 1 app argument")
    else:
        disable_app();
        appname = sys.argv[1] 
        settings = find_settings()
        if( settings ):
            with open(settings,"r") as f:
                content = f.read()
                newconfig = content.replace( "INSTALLED_APPS = [", "INSTALLED_APPS = [\n    '"+appname+"',")
                f.close()
                with open(settings,"w") as g:
                    g.write( newconfig )
        else:
            print( "Cannot locate a settings.py file. Make sure that current directory is a django project folder.")

def disable_app():
    if( len(sys.argv) != 2 ):
        print("Expecting 1 app argument")
    else:
        appname = sys.argv[1] 
        settings = find_settings()
        if( settings ):
            with open(settings,"r") as f:
                content = f.read()
                newconfig = re.sub( r"(INSTALLED_APPS \= \[[\s\S^\]]*?)(\s+'"+appname+"',)", r"\1", content )
                f.close()
                with open(settings,"w") as g:
                    g.write( newconfig )
        else:
            print( "Cannot locate a settings.py file. Make sure that current directory is a django project folder.")
