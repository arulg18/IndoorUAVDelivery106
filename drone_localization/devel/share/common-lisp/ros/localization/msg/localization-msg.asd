
(cl:in-package :asdf)

(defsystem "localization-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "TimestampDistance" :depends-on ("_package_TimestampDistance"))
    (:file "_package_TimestampDistance" :depends-on ("_package"))
  ))