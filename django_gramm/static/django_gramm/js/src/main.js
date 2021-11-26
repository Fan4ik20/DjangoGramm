import 'bootstrap/dist/css/bootstrap.min.css';

import {LikeUnlikeFunc} from "./likeFunc";
import {FollowUnfollowFunc} from "./followFunc";
import {CommentFunc} from "./commentFunc";

window.likeUnlikePost = LikeUnlikeFunc.likeUnlikePost

window.followUnfollow = FollowUnfollowFunc.followUnfollow;

window.deleteComment = CommentFunc.deleteComment;
window.postComment = CommentFunc.postComment;
