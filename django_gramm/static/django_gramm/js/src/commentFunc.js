import {sendRequestAndRefreshContent} from "./requestFunc";
import {parseDataAttrs} from "./parseDataAttrs";


class CommentFunc {
    static deleteComment(deleteTagId) {
        let dataAttrs = parseDataAttrs(deleteTagId);

        sendRequestAndRefreshContent(
            dataAttrs.requestUrl, dataAttrs.divToRefresh,
            "You can\'t delete comment at this moment.",
            "POST"
        )
    }

    static postComment() {
        let dataAttrs = parseDataAttrs('#comment_form')

        let commentForm = document.forms['comment_form'];

        let content = commentForm.elements['content'].value;

        let postData = {'content': content};

        sendRequestAndRefreshContent(
            dataAttrs.requestUrl, dataAttrs.divToRefresh,
            'You cannot post comment at this moment.',
            'POST',
            postData
        );
    }

}


export {CommentFunc};