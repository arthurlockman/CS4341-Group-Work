var   b2Vec2 = Box2D.Common.Math.b2Vec2
     , b2BodyDef = Box2D.Dynamics.b2BodyDef
     , b2Body = Box2D.Dynamics.b2Body
     , b2FixtureDef = Box2D.Dynamics.b2FixtureDef
     , b2Fixture = Box2D.Dynamics.b2Fixture
     , b2World = Box2D.Dynamics.b2World
     , b2MassData = Box2D.Collision.Shapes.b2MassData
     , b2PolygonShape = Box2D.Collision.Shapes.b2PolygonShape
     , b2CircleShape = Box2D.Collision.Shapes.b2CircleShape
     , b2Shape = Box2D.Collision.Shapes.b2Shape
     , b2RevoluteJointDef = Box2D.Dynamics.Joints.b2RevoluteJointDef
     , b2WeldJointDef = Box2D.Dynamics.Joints.b2WeldJointDef
     , b2FilterData = Box2D.Dynamics.b2FilterData
     , b2ContactListener = Box2D.Dynamics.b2ContactListener;


class Character {

     constructor() {

          this.joint = {};
          this.body = {};

          this.l_kneeAngle = 0.175;
          this.r_kneeAngle = 0.175;
          this.l_hipAngle = -0.25;
          this.r_hipAngle = 0.5;
          this.l_hip_rotate_speed = 3;
          this.r_hip_rotate_speed = 3;
          this.l_knee_rotate_speed = 3;
          this.r_knee_rotate_speed = 3;
          this.hipLimits = [-1,1];
          this.kneeLimits = [-0.25,1];

          this.curX = 0.0;
          this.curVelX = 0.0

     }

     /**
       Return 1 if near upper limit, -1 if near lower limit,
       and 0 if not near a limit.
     */
     kneeAtLimit(kneeJoint) {
         if (kneeJoint.GetJointAngle() < this.kneeLimits[0]+0.2) {
             return -1
         } else if (kneeJoint.GetJointAngle() > this.kneeLimits[1]-0.2) {
             return 1
         } else {
            return 0
         }
     }

     /**
       Return 1 if near upper limit, -1 if near lower limit,
       and 0 if not near a limit.
     */
     hipAtLimit(hipJoint) {
         if (hipJoint.GetJointAngle() < this.hipLimits[0]+0.3) {
             return -1
         } else if (hipJoint.GetJointAngle() > this.hipLimits[1]-0.3) {
             return 1
         } else {
            return 0
         }
     }

     shiftBodyX(dx,dy) {
        var self = this.body;
        Object.keys(self).forEach(function(part) {
            var b = self[part];
            var newPos = new b2Vec2(b.GetWorldCenter().x+dx,b.GetWorldCenter().y+dy);
            b.SetPosition(newPos)
         })
     }

     lockRevoluteJoint(joint,torque) {
         torque = torque==undefined ? Infinity : torque;
         joint.SetMaxMotorTorque(torque);
         joint.SetMotorSpeed(0);
         joint.EnableMotor(true)
     }

     /**
       Gets the position on the x axis of the ragdoll's hips. We use
       this as the true forward velocity of the ragdoll instead of
       the center of the torso, since we don't want to reward falling
       forward quickly (at least, not as much as before).
     */
     getHipBaseX() {
         var theta = this.body.torso.GetAngle();
         var x = this.body.torso.GetPosition().x;
         return x - 35*sin(theta)
     }

     getFootY(foot) {
         return (foot.GetUserData()=='ll_leg' ? getLeftFootY() : getRightFootY())
     }

     getLeftFootY(bd) {
         bd = (bd==undefined) ? body : bd;
         return bd.ll_leg.GetPosition().y - (20 * cos(bd.ll_leg.GetAngle()))
     }

     getRightFootY(bd) {
         bd = (bd==undefined) ? body : bd;
         return bd.lr_leg.GetPosition().y - (20 * cos(bd.lr_leg.GetAngle()))
     }

     getFootX(foot) {
         return (foot.GetUserData()=='ll_leg' ? getLeftFootX() : getRightFootX())
     }

     getLeftFootX(bd) {
         bd = (bd==undefined) ? body : bd;
         return bd.ll_leg.GetPosition().x + (20 * sin(bd.ll_leg.GetAngle()))
     }

     getRightFootX(bd) {
         bd = (b2WeldJointDef==undefined) ? body : bd;
         return bd.lr_leg.GetPosition().x + (20 * sin(bd.lr_leg.GetAngle()))
     }

     wrap() {
         this.shiftBodyX(-200,0)
     } 

     translateBody(dx, dy) {
          (Object.keys(body)).forEach(function(elem) {
             var pos = body[elem].GetPosition();
             body[elem].SetType(b2Body.b2_staticBody);
             body[elem].SynchronizeTransform(new b2Vec2(pos.x+dx,pos.y+dy),0);
             body[elem].SetType(b2Body.b2_dynamicBody)
          })
     }

    /**
    * If Q is pressed, rotate the left and right hips. This is done by setting their rotational speed to opposite, constant values.
    */
    handleQPressed() {
        if (this.hipAtLimit(this.joint.l_hip) != 1)
            this.joint.l_hip.SetMotorSpeed(this.l_hip_rotate_speed);
        else
            this.joint.l_hip.SetMotorSpeed(0);
        if (this.hipAtLimit(this.joint.r_hip) != -1)
            this.joint.r_hip.SetMotorSpeed(-this.r_hip_rotate_speed);
        else
            this.joint.r_hip.SetMotorSpeed(0);
    }

    /**
    * If W is pressed, rotate the left and right hips. This is done by setting their rotational speed to opposite, constant values.
    */
    handleWPressed() {
        if (this.hipAtLimit(this.joint.l_hip) != -1)
            this.joint.l_hip.SetMotorSpeed(-this.l_hip_rotate_speed);
        else
            this.joint.l_hip.SetMotorSpeed(0);
        if (this.hipAtLimit(this.joint.r_hip) != 1)
            this.joint.r_hip.SetMotorSpeed(this.r_hip_rotate_speed);
        else
            this.joint.r_hip.SetMotorSpeed(0);
    }

    /** 
    * If O is pressed, rotate the left and right knees. This is done by setting their rotational speeds to opposite, constant values.
    */
    handleOPressed() {
        if (this.kneeAtLimit(this.joint.l_knee) != 1)
            this.joint.l_knee.SetMotorSpeed(this.l_knee_rotate_speed);
        else
            this.joint.l_knee.SetMotorSpeed(0);
        if (this.kneeAtLimit(this.joint.r_knee) != -1)
            this.joint.r_knee.SetMotorSpeed(-this.r_knee_rotate_speed);
        else
            this.joint.r_knee.SetMotorSpeed(0);
    }

    /** 
    * If P is pressed, rotate the left and right knees. This is done by setting their rotational speeds to opposite, constant values.
    */
    handlePPressed() {
        if (this.kneeAtLimit(this.joint.r_knee) != 1)
            this.joint.r_knee.SetMotorSpeed(this.r_knee_rotate_speed);
        else
            this.joint.r_knee.SetMotorSpeed(0);
        if (this.kneeAtLimit(this.joint.l_knee) != -1)
            this.joint.l_knee.SetMotorSpeed(-this.l_knee_rotate_speed);
        else
            this.joint.l_knee.SetMotorSpeed(0);
    }

    handleQReleased() {
        this.joint.l_hip.SetMotorSpeed(0);
        this.joint.r_hip.SetMotorSpeed(0);
        this.l_hipAngle = this.joint.l_hip.GetJointAngle();
        this.r_hipAngle = this.joint.r_hip.GetJointAngle()
    }

    handleWReleased() {
        this.joint.r_hip.SetMotorSpeed(0);
        this.joint.l_hip.SetMotorSpeed(0);
        this.r_hipAngle = this.joint.r_hip.GetJointAngle();
        this.l_hipAngle = this.joint.l_hip.GetJointAngle()
    }

    handleOReleased() {
        this.joint.l_knee.SetMotorSpeed(0);
        this.joint.r_knee.SetMotorSpeed(0);
        this.l_kneeAngle = this.joint.l_knee.GetJointAngle();
        this.r_kneeAngle = this.joint.r_knee.GetJointAngle()
    }

    handlePReleased() {
        this.joint.r_knee.SetMotorSpeed(0);
        this.joint.l_knee.SetMotorSpeed(0);
        this.l_kneeAngle = this.joint.l_knee.GetJointAngle();
        this.r_kneeAngle = this.joint.r_knee.GetJointAngle()
    }    
}
