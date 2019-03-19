#! /usr/bin/env python3

import auth
import group.group
import os

import cgi, cgitb
cgitb.enable()


def redirect_url(user_id, auth_string):
    return "blog.cgi?id={id}&auth={auth}".format(id=user_id, auth=auth_string)


def page(user_id, auth_string, fields):
    print("Content-Type: text/html\n")

    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    if not auth.auth_user(user, auth_string):
        print("<html><body><h1>Not authenticated</h1></body></html>")
        return

    cursor.execute("UPDATE users SET name = %s, rss = %s, type = %s WHERE id = %s",
                   (fields["name"], fields["rss"], fields["type"], user.user_id))
    conn.commit()

    print("""<!DOCTYPE html>                                                    
<html>                                                                          
<body>Updated record.
<a href="{url}">Click here if you aren't automatically redirected.</a>             
<script>                                                                        
var last_slash = location.href.lastIndexOf("/");                                
location.href = location.href.substring(0, last_slash) + "/{url}";                 
</script>                                                                       
</body>                                                                         
</html>                                                                         
""".format(url=redirect_url(user.user_id, auth_string)))

    
def main():
    args = cgi.FieldStorage()
    page(args.getfirst("id"), args.getfirst("auth"),
         {"name": args.getfirst("name"),
          "rss": args.getfirst("rss"),
          "type": args.getfirst("type")})


if __name__ == "__main__":
    main()
