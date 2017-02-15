 // GLOBALS 
var RESET_TIME = 1500
var SIMULATION_SPEED = 1/60

class Game {

    constructor(world, character) {

        this.world = world
        this.character = character
        this.init = false
        this.requestTeleport = false
        this.elapsedTime = 0.0
        this.totalDistTraveled = 0.0
        this.farthestDistTraveled = 0.0
        this.lastInput = [0, 0, 0, 0]
        this.isResetting = true
        this.resetTime = Date.now()
    }

    run(world, character, inputManager, game) {

        // Move everything in the world forward ??
        // The two constants are for position and velocity collision detections
        // Leave as 2
        world.step(SIMULATION_SPEED, 2, 2)

        // Handle key input
        var input = inputManager.getInput()

        // Check to see if resetting
        if(this.isResetting) {
            if(Date.now() - this.resetTime > RESET_TIME) {
                this.isResetting = false
            }
        } else {
            // Handle the input and move the character
            this.handleInput(input)
        }

        // Log this as the last input
        this.lastInput = input

        // Incrememnt elapsed time
        this.elapsedTime += SIMULATION_SPEED

        /* Has reached edge of screen and needs to wrap around */
        if (character.curX > 350) {
            character.wrap()
            character.curX = character.getHipBaseX()
        }

        // Calculate the new position of hip
        var newX = character.getHipBaseX()

        // Calculate the change in position
        var dx = (newX - character.curX)/25

        // Increment the total distance travelled
        this.totalDistTraveled += dx

        // Update the farthest distance travelled
        this.farthestDistTraveled = max(this.farthestDistTraveled, this.totalDistTraveled)

        // Moving forward! 
        if (dx > 0) {
            // notifyForwards
        } 

        /* Moving backwards! */
        else {
            // notifyBackwards
        }

        // Set current and past variables
        character.curX = newX
        character.curVelX = dx/SIMULATION_SPEED

        if (character.body.head.GetPosition().y < 50) {
            // notifyFall
            // Increment death
            this.resetRunner()
        }
    }

    handleInput(input) {
        // Q/W input
        if(input[0]) {this.character.handleQPressed()}
        else if(input[1]) {this.character.handleWPressed()}
        else {this.character.handleQReleased()} // Same as handleWReleased        

        // O/P input
        if(input[2]) {this.character.handleOPressed()}
        else if(input[3]) {this.character.handlePPressed()}
        else {this.character.handleOReleased()} // Same as handlePReleased 
    }

    resetRunner() {

        // Static reference for weird javascript scoping issues
        var self = this

        // Is resetting
        this.isResetting = true
        this.resetTime = Date.now()

        // Has already been initialized at least once
        if (this.init) {
            Object.keys(self.character.body).forEach( function(part) {
                self.world.world.DestroyBody(self.character.body[part])
            })
            Object.keys(self.character.joint).forEach( function(part) {
                self.world.world.DestroyJoint(self.character.joint[part])
            })

            this.elapsedTime = 0.0
            this.totalDistTraveled = 0.0
        }

        this.init = true

        this.character.joint = {}
        this.character.body = {}

        this.character.l_kneeAngle = 0.175
        this.character.r_kneeAngle = 0.175
        this.character.l_hipAngle = -0.25
        this.character.r_hipAngle = 0.5

        // Create all body parts
        var head = this.world.createBall(250, 160, 25, false, 0.1)
        var l_arm = this.world.createBox(202, 126, 40, 8, 0, false, 0.1)
        var ul_leg = this.world.createBox(248, 44, 10, 40, PI/6, false, 10)
        var ll_leg = this.world.createBox(248, 16, 10, 40, -PI/6, false, 10)
        var torso = this.world.createBox(234, 68, 32, 70, 0, false, 5)
        var r_arm = this.world.createBox(258, 126, 40, 8, 0, false, 0.1)
        var ur_leg = this.world.createBox(248, 44, 10, 40, PI/6, false, 10)
        var lr_leg = this.world.createBox(248, 16, 10, 40, -PI/6, false, 10)

        // Track joints and body components
        this.character.body.head = head
        this.character.body.torso = torso
        this.character.body.l_arm = l_arm
        this.character.body.r_arm = r_arm
        this.character.body.ll_leg = ll_leg
        this.character.body.ul_leg = ul_leg
        this.character.body.lr_leg = lr_leg
        this.character.body.ur_leg = ur_leg
        head.SetUserData('head')
        torso.SetUserData('torso')
        l_arm.SetUserData('l_arm')
        r_arm.SetUserData('r_arm')
        ll_leg.SetUserData('ll_leg')
        ul_leg.SetUserData('ul_leg')
        lr_leg.SetUserData('lr_leg')
        ur_leg.SetUserData('ur_leg')

        // Connect head and torso
        var neck_jointDef = new b2WeldJointDef()
        var neck_anchor = head.GetWorldCenter()
        neck_anchor.y = neck_anchor.y - 20
        neck_jointDef.Initialize(head, torso, neck_anchor)
        var neck_joint = this.world.world.CreateJoint(neck_jointDef)

        // Connect left arm to torso
        var l_arm_jointDef = new b2RevoluteJointDef()
        var l_arm_anchor = l_arm.GetWorldCenter()
        l_arm_anchor.x = l_arm_anchor.x + 15
        l_arm_jointDef.Initialize(l_arm, torso, l_arm_anchor)
        var l_arm_joint = this.world.world.CreateJoint(l_arm_jointDef)

        // Connect right arm to torso
        var r_arm_jointDef = new b2RevoluteJointDef()
        var r_arm_anchor = r_arm.GetWorldCenter()
        r_arm_anchor.x = r_arm_anchor.x - 15
        r_arm_jointDef.Initialize(r_arm, torso, r_arm_anchor)
        var r_arm_joint = this.world.world.CreateJoint(r_arm_jointDef)

        // Connect upper, lower left leg
        var l_knee_jointDef = new b2RevoluteJointDef()
        var l_knee_anchor = ul_leg.GetWorldCenter()
        l_knee_anchor.x = l_knee_anchor.x + 8.25
        l_knee_anchor.y = l_knee_anchor.y - 14.3
        l_knee_jointDef.Initialize(ul_leg, ll_leg, l_knee_anchor)
        var l_knee_joint = this.world.world.CreateJoint(l_knee_jointDef)

        // Connect upper, lower right leg
        var r_knee_jointDef = new b2RevoluteJointDef()
        var r_knee_anchor = ur_leg.GetWorldCenter()
        r_knee_anchor.x = r_knee_anchor.x + 8.25
        r_knee_anchor.y = r_knee_anchor.y - 14.3
        r_knee_jointDef.Initialize(ur_leg, lr_leg, r_knee_anchor)
        var r_knee_joint = this.world.world.CreateJoint(r_knee_jointDef)

        // Attach left, right legs to torso
        var l_hip_jointDef = new b2RevoluteJointDef()
        var l_hip_anchor = ul_leg.GetWorldCenter()
        l_hip_anchor.x = l_hip_anchor.x - 12
        l_hip_anchor.y = l_hip_anchor.y + 26
        l_hip_jointDef.Initialize(torso, ul_leg, l_hip_anchor)
        var l_hip_joint = this.world.world.CreateJoint(l_hip_jointDef)

        var r_hip_jointDef = new b2RevoluteJointDef()
        var r_hip_anchor = ur_leg.GetWorldCenter()
        r_hip_anchor.x = r_hip_anchor.x - 12
        r_hip_anchor.y = r_hip_anchor.y + 26
        r_hip_jointDef.Initialize(torso, ur_leg, r_hip_anchor)
        var r_hip_joint = this.world.world.CreateJoint(r_hip_jointDef)

        // body.l_foot = l_foot
        // body.r_foot = r_foot
        this.character.joint.neck = neck_joint
        this.character.joint.l_arm = l_arm_joint
        this.character.joint.r_arm = r_arm_joint
        this.character.joint.l_hip = l_hip_joint
        this.character.joint.r_hip = r_hip_joint
        this.character.joint.l_knee = l_knee_joint
        this.character.joint.r_knee = r_knee_joint

        // Prevent arms, legs from colliding with each other
        this.setFilterGroup([l_arm,r_arm,this.world.environment.floor],-1)
        this.setFilterGroup([torso,ul_leg,ur_leg,ll_leg,lr_leg],-2)

        // Stiffen hip, arm and knee joints
        this.character.lockRevoluteJoint(l_knee_joint)
        this.character.lockRevoluteJoint(r_knee_joint)
        this.character.lockRevoluteJoint(l_hip_joint)
        this.character.lockRevoluteJoint(r_hip_joint)
        this.character.lockRevoluteJoint(l_arm_joint,8000)
        this.character.lockRevoluteJoint(r_arm_joint,8000)

        /* Resets the runner to stable standing position */
        setInterval(function() {

            var r = l_hip_joint.GetJointAngle()
            l_hip_joint.SetMotorSpeed(2*(self.character.l_hipAngle - r))

            r = r_hip_joint.GetJointAngle()
            r_hip_joint.SetMotorSpeed(2*(self.character.r_hipAngle - r))

            var r = l_knee_joint.GetJointAngle()
            l_knee_joint.SetMotorSpeed(2*(self.character.l_kneeAngle - r))

            r = r_knee_joint.GetJointAngle()
            r_knee_joint.SetMotorSpeed(2*(self.character.r_kneeAngle - r))

        },100)

        l_hip_joint.EnableLimit(true)
        l_hip_joint.SetLimits(this.character.hipLimits[0],this.character.hipLimits[1])   // -1 and 1
        r_hip_joint.EnableLimit(true)
        r_hip_joint.SetLimits(this.character.hipLimits[0],this.character.hipLimits[1])
        l_knee_joint.EnableLimit(true)
        l_knee_joint.SetLimits(this.character.kneeLimits[0], this.character.kneeLimits[1])    // -0.25 and 1
        r_knee_joint.EnableLimit(true)
        r_knee_joint.SetLimits(this.character.kneeLimits[0], this.character.kneeLimits[1])

        this.character.curVelX = 0.0
        this.character.curX = this.character.getHipBaseX()
    }

    // Used to prevent arms, legs from colliding with each other
    setFilterGroup(elems, fIndex) {
        elems.forEach(function(elem) {
            var fList = elem.GetFixtureList()
            var filterData = fList.GetFilterData()
            filterData.groupIndex = fIndex
            fList.SetFilterData(filterData)
        })
    }

}