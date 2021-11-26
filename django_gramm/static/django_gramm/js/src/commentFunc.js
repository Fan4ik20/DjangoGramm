import {_sendRequestAndCheckStatus} from "./requestFunc";
import {parseDataAttrs} from "./parseDataAttrs";


class CommentFunc {
    static _sendDeleteRequestAndRemoveComment(url, commentTagId) {
        let commentTag = $(commentTagId)

        try {
            _sendRequestAndCheckStatus(url, 'POST').done(() => {
                commentTag.remove();
            })
        }

        catch (error) {
            alert('You can\'t delete this comment at this moment.');
        }
    }


    static deleteComment(deleteTagId) {
        let dataAttrs = parseDataAttrs(
            deleteTagId, 'requestUrl', 'commentTagId'
        );

        CommentFunc._sendDeleteRequestAndRemoveComment(
            dataAttrs['requestUrl'], dataAttrs['commentTagId']
        );
    }


    static _updateComments(commentsTag, commentData) {
        let newCommentHtml = $('#hidden_comment_template').clone().attr(
            'id', `comment_${commentData['id']}`
        ).css('display', 'block');


        let tagChildren = newCommentHtml.children();
        let [userImage, usernameLink,
            commentCreatedDate, commentContent, deleteComment] = tagChildren;


        if (commentData['user']['user_picture']) {
            $(userImage).attr('src', commentData['user_picture']);
        }


        $(usernameLink).attr(
            'href', `/users/${commentData['user']['username']}/`
        );
        $(usernameLink).children()[0].innerHTML = commentData['user']['username'];


        let date = new Date(commentData['created_time']);
        let formattedDate = `${date.getHours()}:${date.getMinutes()}
         ${date.getDay()}/${date.getMonth()} ${date.getFullYear()}`;

        $(commentCreatedDate).text(formattedDate);


        $(commentContent).children()[0].innerHTML = commentData['content'];


        $(deleteComment).attr(
            {
                'id': `delete_comment_${commentData['id']}`,
                'onclick': `deleteComment('#delete_comment_${commentData['id']}')`,
                'data-request-url': `/users/${commentData['user']['username']}/posts/${commentData['post_id']}/comments/${commentData['id']}/delete/`,

                'data-comment-tag-id': `#comment_${commentData['id']}`
            }
        );

        newCommentHtml.appendTo(commentsTag);
    }


    static _sendRequestAndUpdateComments(url, postData, commentsId) {
        let commentsTag = $(commentsId);

        try {
            _sendRequestAndCheckStatus(url, 'POST', postData).done(
                (jsonResponse) => {
                    console.log(jsonResponse);
                    CommentFunc._updateComments(commentsTag, jsonResponse['comment']);
                }
            );


        }

        catch (error) {
            alert('You cannot post comment at this moment.')
        }
    }


    static postComment(tagToParse) {
        let dataAttrs = parseDataAttrs(
            tagToParse, 'postCommentUrl', 'commentsId'
        )

        let commentForm = document.forms['comment_form'];

        let content = commentForm.elements['content'].value;
        commentForm.elements['content'].value = '';

        let postData = {'content': content};

        CommentFunc._sendRequestAndUpdateComments(
            dataAttrs['postCommentUrl'], postData, dataAttrs['commentsId']
        );
    }

}


export {CommentFunc};