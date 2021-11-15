import {sendRequestAndRefreshContent} from "./requestFunc";
import {parseDataAttrs} from "./parseDataAttrs";


class FollowUnfollowFunc {
    static followUser() {
        let dataAttrs = parseDataAttrs("#follow_user");

        sendRequestAndRefreshContent(
            dataAttrs.requestUrl, dataAttrs.divToRefresh,
            "You cant to follow this user at this moment."
        );
    }

    static unfollowUser() {
        let dataAttrs = parseDataAttrs("#unfollow_user");

        sendRequestAndRefreshContent(
            dataAttrs.requestUrl, dataAttrs.divToRefresh,
            "You cant to unfollow this user at this moment."
        );
    }
}


export {FollowUnfollowFunc};