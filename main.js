// const command ='curl -X GET -u elastic:ysnwxOkXJrhrSDFINyQPoBnF "https://<servername>/<index-name>/_search?pretty" -H "Content-Type: application/json" -d"{"query": {"match": {"html": "test"}}}"'
function searchword() {
    const url = '-u elastic:ysnwxOkXJrhrSDFINyQPoBnF "https://<servername>/<index-name>/_search?pretty" -H "Content-Type: application/json" -d"{"query": {"match": {"html": "test"}}}"'

    $.ajax({
        url: url,
        success: function(data) {
            console.log(data)
        }
    });
}
