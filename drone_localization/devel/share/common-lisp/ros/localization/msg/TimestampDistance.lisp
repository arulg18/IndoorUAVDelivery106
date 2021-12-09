; Auto-generated. Do not edit!


(cl:in-package localization-msg)


;//! \htmlinclude TimestampDistance.msg.html

(cl:defclass <TimestampDistance> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (distance
    :reader distance
    :initarg :distance
    :type cl:float
    :initform 0.0))
)

(cl:defclass TimestampDistance (<TimestampDistance>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TimestampDistance>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TimestampDistance)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name localization-msg:<TimestampDistance> is deprecated: use localization-msg:TimestampDistance instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <TimestampDistance>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader localization-msg:header-val is deprecated.  Use localization-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'distance-val :lambda-list '(m))
(cl:defmethod distance-val ((m <TimestampDistance>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader localization-msg:distance-val is deprecated.  Use localization-msg:distance instead.")
  (distance m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TimestampDistance>) ostream)
  "Serializes a message object of type '<TimestampDistance>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'distance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TimestampDistance>) istream)
  "Deserializes a message object of type '<TimestampDistance>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'distance) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TimestampDistance>)))
  "Returns string type for a message object of type '<TimestampDistance>"
  "localization/TimestampDistance")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TimestampDistance)))
  "Returns string type for a message object of type 'TimestampDistance"
  "localization/TimestampDistance")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TimestampDistance>)))
  "Returns md5sum for a message object of type '<TimestampDistance>"
  "4c739b0ad83c2914df6d41fe1b87d25f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TimestampDistance)))
  "Returns md5sum for a message object of type 'TimestampDistance"
  "4c739b0ad83c2914df6d41fe1b87d25f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TimestampDistance>)))
  "Returns full string definition for message of type '<TimestampDistance>"
  (cl:format cl:nil "Header header~%float32 distance~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TimestampDistance)))
  "Returns full string definition for message of type 'TimestampDistance"
  (cl:format cl:nil "Header header~%float32 distance~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TimestampDistance>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TimestampDistance>))
  "Converts a ROS message object to a list"
  (cl:list 'TimestampDistance
    (cl:cons ':header (header msg))
    (cl:cons ':distance (distance msg))
))
