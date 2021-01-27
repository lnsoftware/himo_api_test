release = 'https://mainto-app-1-0.local.hzmantu.com/'

# Token
app_get_token = 'user_auth/getTokenFromApp'
login_by_token = 'user_auth/login/token'
logout = 'user_auth/logout'

# 排单表
getMultiStoreReservations = 'project_mainto_app/product/getMultiStoreReservations/v1'
getReservationList = 'project_mainto_app/product/getReservationList/v1'

# 优惠券
getUserPreferentialCard = 'project_mainto_app/user/getUserPreferentialCard/v1'
unusedCoupons = 'project_mainto_app/user/preferentialCard/availableList/v1'
coupons_productCard = 'project_mainto_app/user/preferentialCard/availableListAll/v1'
spring_coupons = 'project_mainto_app/user/preferentialCard/bindSpringCoupon/v1'
spring_status = 'project_mainto_app/user/preferentialCard/springCouponInfo/v1'

# NPS问卷
nps_creat = 'project_mainto_app/order/nps/create/v1'
nps_status = 'project_mainto_app/order/nps/status/v1'

# 用户信息
feedback = 'project_mainto_app/user/feedback/v1'  # 意见反馈
userFlow = 'project_mainto_app/user/userFlow/v1'  # 纪念值
userInfo = 'project_mainto_app/user/userinfo/v1'  # 用户信息
userWalfare = 'project_mainto_app/user/userWalfareList/v1'  # 获得会员卡列表权益
protocolVersion = 'project_mainto_app/user/protocolVersion/v1'  # 预约协议版本
changeUserPassword = 'project_mainto_app/user/changUserPassword/v1'  # 修改密码
cardCreat = 'project_mainto_app/user/cardCreate/v1'  # 生成微信会员卡
alertCheck = 'project_mainto_app/user/alertCheck/v1'  # 用户vip升级弹框标记
editUserInfo = 'project_mainto_app/user/userinfo/edit/v1'  # 修改用户信息

# 订单信息
deleteOrder = 'project_mainto_app/order/delete/v1'
orderCancel = 'project_mainto_app/order/cancel/v1'
changeReserveTime = 'project_mainto_app/user/order/changeReserveTime/v1'
createOrder = 'project_mainto_app/order/create/v1'
orderDetail = 'project_mainto_app/order/detail/v1'
orderList = 'project_mainto_app/order/list/v1'
oderRefundReason = 'project_mainto_app/order/refund/reason/v1'
orderRefundToGiftCard = 'project_mainto_app/order/refundToGiftCard/v1'
order_getSubOrderServiceComplteInfo = 'project_mainto_app/order/subOrder/getSubOrderServiceCompleteInfo/v1'
orderPhoto = 'project_mainto_app/order/photo/v1'
orderSubOrder = 'project_mainto_app/order/subOrder/serviceCompleteInfo/v1'

# 电子发票
invoiceHistory = 'project_mainto_app/user/invoice/history/v1'
invoiceList = 'project_mainto_app/user/invoice/list/v1'
invoiceHmx = 'project_mainto_app/user/invoice/storeHmx/v1'

# 商品信息
productDetail = 'project_mainto_app/product/getBatchDetailByProductIds/v1'
allCategoriesByStoreId = 'project_mainto_app/product/getAllCategoriesByStoreId/v1'
productCategoryByStoreIdAndCatId = 'project_mainto_app/product/getProductCategoryByStoreIdAndCatId/v1'
hotProducts = 'project_mainto_app/product/getHotProducts/v1'
productDiscountDetailByStoreId = 'project_mainto_app/product/getProductDiscountDetailByStoreId/v1'
productTips = 'project_mainto_app/product/getProductTips/v1'
youLike = 'project_mainto_app/product/getProductYouLike/v1'

# 礼品卡
giftCardCancel = 'project_mainto_app/user/giftCard/cancel/v1'
giftCardCharge = 'project_mainto_app/user/giftCard/charge/v1'
giftCardConfirm = 'project_mainto_app/user/giftCard/confirm/v1'
giftCardBuy = 'project_mainto_app/user/giftCard/buy/v1'
giftCardCoverList = 'project_mainto_app/user/giftCard/coverList/v1'
giftCardChargeRecord = 'project_mainto_app/user/giftCard/chargeRecord/v1'
giftCardOrderDetail = 'project_mainto_app/user/giftCard/orderDetail/v1'
giftCardOrderList = 'project_mainto_app/user/giftCard/orderList/v1'
giftCardTransactionList = 'project_mainto_app/user/giftCard/transactionList/v1'
giftCardGetGiftCards = 'project_mainto_app/user/getGiftCards/v1'
giftCardGive = 'project_mainto_app/user/giftCard/give/v1'
giftCardGiveDetail = 'project_mainto_app/user/giftCard/giveDetail/v1'
giftCardTopicList = 'project_mainto_app/user/giftCard/topicList/v1'
giftCardInfo = 'project_mainto_app/user/giftCard/info/v1'
getUserGiftCards = 'project_mainto_app/user/getUserGiftCards/v1'
giftCardPreview = 'project_mainto_app/user/giftCard/preview/v1'
gifrCardReceive = 'project_mainto_app/user/giftCard/receive/v1'
giftCardSetCover = 'project_mainto_app/user/giftCard/setCover/v1'
