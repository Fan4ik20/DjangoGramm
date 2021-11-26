import {_sendRequestAndCheckStatus} from "./requestFunc";
import {parseDataAttrs} from "./parseDataAttrs";


class FollowUnfollowFunc {
    static _sendRequestAndChangeFollowStatus(
        urlToRequest, tagIdToChange, newTagValue, alertMessage, followersCountTag) {

        try {
            _sendRequestAndCheckStatus(urlToRequest);

            let tag = $(tagIdToChange);

            tag.text(newTagValue);

            if (followersCountTag) {
                let followersCount = parseInt(followersCountTag.text());
                let newFollowersCount = (
                    newTagValue === 'Unfollow' ? ++followersCount : -- followersCount
                );

                followersCountTag.text(newFollowersCount);
            }
        }

        catch (error) {
            alert(alertMessage);
        }
    }

    static _checkFollowUnfollowAndCallRequest(tagIdToChange, dataAttrs) {
        let tagToChange = $(tagIdToChange);
        let followersCountTag = $(dataAttrs['followersCountId']);

        let tagText = $.trim(tagToChange.text());

        if (tagText.toLowerCase() === 'follow') {
            FollowUnfollowFunc._sendRequestAndChangeFollowStatus(
                dataAttrs['followUrl'], tagIdToChange,
                'Unfollow', 'You can\t to follow this user at this moment',
                followersCountTag
            );
        }

        else if (tagText.toLowerCase() === 'unfollow') {
            FollowUnfollowFunc._sendRequestAndChangeFollowStatus(
                dataAttrs['unfollowUrl'], tagIdToChange,
                'Follow', 'You can\t to unfollow this user at this moment',
                followersCountTag
            );
        }
    }


    static followUnfollow(tagIdToParse, tagIdToChange) {
        let dataAttrs = parseDataAttrs(
            tagIdToParse, 'followUrl', 'unfollowUrl',
            'followersCountId'
        );

        FollowUnfollowFunc._checkFollowUnfollowAndCallRequest(
            tagIdToChange, dataAttrs
        );

    }
}

export {FollowUnfollowFunc};