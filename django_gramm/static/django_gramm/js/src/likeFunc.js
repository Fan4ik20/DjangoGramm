import {sendRequestAndRefreshContent} from './requestFunc'
import {parseDataAttrs} from "./parseDataAttrs";


class LikeUnlikeFunc {
    static _sendRequest(dataAttrs, message) {
        sendRequestAndRefreshContent(
            dataAttrs.requestUrl, dataAttrs.divToRefresh,
            message
        )

    }

    static likePost(likeTagId) {
        let dataAttrs = parseDataAttrs(likeTagId);

        LikeUnlikeFunc._sendRequest(dataAttrs,
            'You cannot like this post at this moment.')
    }

        static unlikePost(unlikeTagId) {
            let dataAttrs = parseDataAttrs(unlikeTagId);

            LikeUnlikeFunc._sendRequest(dataAttrs,
            'You cannot unlike this post at this moment.')
    }
}

export {LikeUnlikeFunc};
