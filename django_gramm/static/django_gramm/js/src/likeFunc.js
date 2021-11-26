import {
    _sendRequestAndCheckStatus
} from './requestFunc'

import {parseDataAttrs} from "./parseDataAttrs";


class LikeUnlikeFunc {
    static _sendRequestAndChangeCssClass(
        urlToRequest, likeTag, classToAdd, classToRemove,
        alertMessage, likesCountTag) {

        try {
            _sendRequestAndCheckStatus(urlToRequest).done(() => {
                likeTag.removeClass(classToRemove);
                likeTag.addClass(classToAdd);

                if (likesCountTag) {
                    let likesCount = parseInt(likesCountTag.text())
                    let newLikesCount = classToAdd === 'liked' ? ++likesCount : --likesCount;

                    likesCountTag.text(newLikesCount);

                }
            })
        }

        catch (error) {
            alert(alertMessage);
        }
    }

    static _checkLikedUnlikedCssClassesAndCallRequest(likeTagId, dataAttrs) {
        let likeTag = $(likeTagId);
        let likesCountTag = $(dataAttrs['likesCountId'])

        if (likeTag.hasClass('liked')) {
            LikeUnlikeFunc._sendRequestAndChangeCssClass(
                dataAttrs['unlikeUrl'], likeTag, 'unliked', 'liked',
                'You can\'t unlike this post at this moment.',
                likesCountTag
            );
        }

        else if (likeTag.hasClass('unliked')) {
            LikeUnlikeFunc._sendRequestAndChangeCssClass(
                dataAttrs['likeUrl'], likeTag, 'liked', 'unliked',
                'You can\'t like this post at this moment.',
                likesCountTag
            );
        }
    }

    static likeUnlikePost(tagIdToParse, likeUnlikeTagId) {
        let dataAttrs = parseDataAttrs(tagIdToParse,
            'likeUrl', 'unlikeUrl', 'likesCountId');

        LikeUnlikeFunc._checkLikedUnlikedCssClassesAndCallRequest(
            likeUnlikeTagId, dataAttrs
        );
    }
}


export {LikeUnlikeFunc};
