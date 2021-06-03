function search(object) {
    document.getElementById('resultdiv').innerHTML =''

    const value =object.value
    object.value =''

    const command ='curl -X GET -u elastic:ysnwxOkXJrhrSDFINyQPoBnF "https://cs172-69dc7d.es.us-west1.gcp.cloud.es.io:9243/cs172-index/_search?pretty" -H \'Content-Type: application/json\' -d\'{"query": {"match": {"html": "' +value +'"}}}\''

    arr =value.split(' ');

    require('child_process').exec(command, function(err, data, stderr) { 
        data =JSON.parse(data);

        console.log(data);

        hits =data['hits']['hits'];

        hits.sort((a, b) => (a._score < b._score) ? 1 : -1)

        for(var i =0; i <hits.length; i++) {
            var text =hits[i]['_source']['html']

            text =makeBold(arr, text);

            displayData(hits[i]['_score'], text)
        }
    });
}

function makeBold(arr, text) {
    for(var i =0; i <arr.length; i++) {
        text =text.replace(arr[i], '<b>' +arr[i] +'</b>');
    }

    return text;
}

function displayData(score, text) {
    const datadiv =document.createElement('div');
    datadiv.className ="textcontent"

    datadiv.innerHTML ='score =' +score +'<br>' +'text: \n' +text

    document.getElementById('resultdiv').appendChild(datadiv);
}