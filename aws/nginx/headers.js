function headers_json(r) {
   var a, s, h;

    s = "JS summary";

    s += "Method: " + r.method + ", ";
    s += "HTTP version: " + r.httpVersion + ", ";
    s += "Host: " + r.headersIn.host + ", ";
    s += "Remote Address: " + r.remoteAddress + ", ";
    s += "URI: " + r.uri + ", ";

    s += "Headers:";
    for (h in r.headersIn) {
        s += "  header '" + h + "' is '" + r.headersIn[h] + "', ";
    }

    s += "Args:";
    for (a in r.args) {
        s += "  arg '" + a + "' is '" + r.args[a] + "' ";
    }
  r.log(s);
  return s;
}

export default {headers_json};
