function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function _refreshDiv(divId) {
    $(divId).html = $(divId).load(document.URL + ` ${divId}>*`);
}


function _checkResponseStatus(response) {
    response.done(function (jsonResponse) {
        if (jsonResponse.status !== 'OK') {
            throw new Error("Something went wrong! Status != 'OK'");
        }

        if (jsonResponse.code !== 200) {
            throw new Error("Something went wrong! Code != '200'");
        }
    })
}


function _sendRequestAndCheckStatus(url, method, postData) {
    let response;
    try {
        if (method){
            let csrftoken;
            let options = {'method': method};

            if (method === 'POST' || method === 'DELETE') {
                csrftoken = getCookie('csrftoken');
                options.headers = {'X-CSRFToken': csrftoken};
            }

            if (method === 'POST' && postData) {
                options.data = postData;
            }


            response = $.ajax(
                url, options
            )

    }

    else {
        response = $.get(url)
        }
    }

    catch (error) {
        throw new Error("The request failed");
    }


    _checkResponseStatus(response);

    return response;
}


function sendRequestAndRefreshContent(
    url, divId, message, method, postData
){
    try {
        _sendRequestAndCheckStatus(url, method, postData).done(function() {
            _refreshDiv(divId);
        })
    }

    catch (err) {
        console.log(err);
        alert(message);
    }
}

export {sendRequestAndRefreshContent, _sendRequestAndCheckStatus}
