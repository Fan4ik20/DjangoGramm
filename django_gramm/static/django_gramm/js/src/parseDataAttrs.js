function parseDataAttrs(tagIdToParse, ...argumentsToParse) {
    let tag = $(tagIdToParse);

    let dataArgs = {};

    argumentsToParse.forEach((arg) => {
        dataArgs[arg] = tag.data(arg);
    });

    return dataArgs;
}


export {parseDataAttrs}