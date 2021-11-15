function parseDataAttrs(tagIdToParse) {
    let tag = $(tagIdToParse);

    let requestUrl = tag.data("requestUrl");
    let divToRefresh = tag.data("divToRefresh")

    return {requestUrl: requestUrl, divToRefresh: divToRefresh}
}


export {parseDataAttrs}