package lib

import (
	"net/http"
	"net/url"
	"fmt"
	"strconv"
	"errors"
	"github.com/julienschmidt/httprouter"
)

var (
	httpCodes = map[int]string{
		100: "Continue",
		101: "Switching Protocols",
		102: "Processing",
		// LEVEL 200
		200: "OK",
		201: "Created",
		202: "Accepted",
		203: "Non-Authoritative Information",
		204: "No Content",
		205: "Reset Content",
		206: "Partial Content",
		207: "Multi-Status",
		// LEVEL 300
		300: "Multiple Choices",
		301: "Moved Permanently",
		302: "Found",
		303: "See Other",
		304: "Not Modified",
		305: "Use Proxy",
		306: "unused",
		307: "Temporary Redirect",
		// LEVEL 400
		400: "Bad Request",
		401: "Authorization Required",
		402: "Payment Required",
		403: "Forbidden",
		404: "Not Found",
		405: "Method Not Allowed",
		406: "Not Acceptable",
		407: "Proxy Authentication Required",
		408: "Request Time-out",
		409: "Conflict",
		410: "Gone",
		411: "Length Required",
		412: "Precondition Failed",
		413: "Request Entity Too Large",
		414: "Request-URI Too Large",
		415: "Unsupported Media Type",
		416: "Requested Range Not Satisfiable",
		417: "Expectation Failed",
		418: "unused",
		419: "unused",
		420: "unused",
		421: "unused",
		422: "Unprocessable Entity",
		423: "Locked",
		424: "Failed Dependency",
		425: "No code",
		426: "Upgrade Required",
		// LEVEL 500
		500: "Internal Server Error",
		501: "Method Not Implemented",
		502: "Bad Gateway",
		503: "Service Temporarily Unavailable",
		504: "Gateway Time-out",
		505: "HTTP Version Not Supported",
		506: "Variant Also Negotiates",
		507: "Insufficient Storage",
		508: "unused",
		509: "unused",
		510: "Not Extended",
	}
)

const (
	BANNER = "Apache/2.2.15 (CentOS)"
	EMAIL = "admin@exist.not"
	TEMPLATE = `<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>%d %s</title>
</head><body>
<h1>%s</h1>
%s<hr>
<address>%s Server at %s Port %d</address>
</body></html>`
)

func getServerInfo(req *http.Request) (code int, uri, host, title, msg string, port uint16, err error) {
	realUri := req.RequestURI
	l := len(realUri)
	code, err = strconv.Atoi(realUri[l - 3 : l])
	if err != nil {
		return
	}
	fmt.Printf("code = %d\n", code)
	if _, ok := req.Header["X-Request-Uri"]; ok {
		uri = req.Header.Get("X-Request-Uri")
	} else {
		uri = realUri
	}
	//fmt.Printf("uri = %s, length = %d\n", uri, len(uri))
	switch code {
	case 401:
		msg = `<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>`
	case 403:
		msg = fmt.Sprintf(`<p>You don't have permission to access %s on this server.</p>`, uri)
	case 404:
		msg = fmt.Sprintf(`<p>The requested URL %s was not found on this server.</p>`, uri)
	case 500:
		msg = fmt.Sprintf(`<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator, %s and inform them of the time the error occurred,
and anything you might have done that may have
caused the error.</p>
<p>More information about this error may be available
in the server error log.</p>`, EMAIL)
	default:
		err = errors.New("code not permitted")
		return
	}
	title = httpCodes[code]
	//fmt.Printf("title = %s, length = %d\n", title, len(title))

	xHost := false
	xPort := false
	if _, ok := req.Header["X-Server-Host"]; ok {
		xHost = true
	}
	if _, ok := req.Header["X-Server-Port"]; ok {
		xPort = true
	}

	strPort := "80"
	if xHost && xPort {
		host = req.Header.Get("X-Server-Host")
		strPort = req.Header.Get("X-Server-Port")
	} else {
		rawUrl := "http://" + req.Host + req.RequestURI
		u, urlErr := url.Parse(rawUrl)
		if urlErr == nil {
			strPort = u.Port()
			host = u.Hostname()
		}
	}
	//fmt.Printf("host = %s, length = %d\n", host, len(host))

	//fmt.Printf("strPort = %s\n", strPort)
	iPort, portErr := strconv.Atoi(strPort)
	if portErr != nil || iPort <= 0 || iPort > 65535 {
		port = 80 // ?
	} else {
		port = uint16(iPort)
	}
	//fmt.Printf("port = %v\n", port)
	return
}

func ResponseCode(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	code, _, host, title, msg, port, err := getServerInfo(r)
	if err != nil {
		fmt.Println(err)
		return
	}
	html := fmt.Sprintf(TEMPLATE, code, title, title, msg, BANNER, host, port)
	fmt.Fprint(w, html)
}
