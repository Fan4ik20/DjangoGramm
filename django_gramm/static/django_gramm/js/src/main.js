import 'bootstrap/dist/css/bootstrap.min.css';

import {LikeUnlikeFunc} from "./likeFunc";
import {FollowUnfollowFunc} from "./followFunc";
import {CommentFunc} from "./commentFunc";


window.likePost = LikeUnlikeFunc.likePost;
window.unlikePost = LikeUnlikeFunc.unlikePost;

window.followUser = FollowUnfollowFunc.followUser;
window.unfollowUser = FollowUnfollowFunc.unfollowUser;

window.deleteComment = CommentFunc.deleteComment;
window.postComment = CommentFunc.postComment;
