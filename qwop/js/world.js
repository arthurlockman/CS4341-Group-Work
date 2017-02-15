

class World {

    constructor(worldWidth, worldHeight, character) {

        this.worldWidth = worldWidth
        this.worldHeight = worldHeight
        this.character = character

        var gravity = new b2Vec2(0, -75)
        this.world = new b2World(gravity, true)

        this.environment = this.initWalls(24)

        var listener = new b2ContactListener()
        var env = this.environment
        var bd = this.character.body

        listener.PreSolve = function(contact, oldManifold) {
            var body_A = contact.GetFixtureA().GetBody()
            var body_B = contact.GetFixtureB().GetBody()
            if (body_A == env.r_wall || body_B == env.r_wall) {
                requestTeleport = true
            } else if (autoReset) {
                if (body_A == env.floor) {
                    if (body_B !== bd.ll_leg && body_B !== bd.ul_leg &&
                     body_B !== bd.lr_leg && body_B !== bd.ur_leg) {
                        requestReset = true
                    }
                } else if (body_B == env.floor) {
                    if (body_A !== bd.ll_leg && body_A !== bd.ul_leg &&
                     body_A !== bd.lr_leg && body_A !== bd.ur_leg) {
                        requestReset = true
                    }
                }
            }
        }

        this.world.SetContactListener(listener)

    }

    step(freq, param1, param2) {
        this.world.Step(freq,param1,param2)
    }

    initWalls(t) {

        // Create the floor
        var floor = this.createBox(0, -t/2, this.worldWidth, t, 0, true)
        floor.SetUserData('floor')

        // Create the left wall; Only god knows what these parameters are
        var l_wall = this.createBox(-t/2, 0, t, this.worldHeight, 0, true)
        l_wall.SetUserData('l_wall')

        // Create the right wall; Only god knows what these parameters are
        var r_wall = this.createBox(this.worldWidth-t/2, 0, t, this.worldHeight, 0, true)
        r_wall.SetUserData('r_wall')

        return {'floor':floor, 'l_wall':l_wall, 'r_wall':r_wall}
    }

    createBall(x, y, radius, fixed, density) {

        radius = 20

        var bodyDef = new b2BodyDef()
        var fixDef = new b2FixtureDef()

        fixDef.density = density==undefined ? 1 : density
        fixDef.friction = 5
        fixDef.restitution = 0.5

        bodyDef.type = fixed ? b2Body.b2_staticBody : b2Body.b2_dynamicBody

        fixDef.shape = new b2CircleShape(radius)

        bodyDef.position.x = x
        bodyDef.position.y = y

        this.world.CreateBody(bodyDef).CreateFixture(fixDef)
        return this.world.GetBodyList()
    }

    createPolygon(x, y, points, fixed, density) {

        var bodyDef = new b2BodyDef()
        var fixDef = new b2FixtureDef()

        fixDef.density = density==undefined ? 1 : density
        fixDef.friction = 15
        fixDef.restitution = 1

        bodyDef.type = fixed ? b2Body.b2_staticBody : b2Body.b2_dynamicBody

        fixDef.shape = new b2PolygonShape()
        fixDef.shape.SetAsArray(
            points.map( function (point) {
                return new b2Vec2(point.x, point.y)
            })
        )

        bodyDef.position.x = x
        bodyDef.position.y = y

        this.world.CreateBody(bodyDef).CreateFixture(fixDef)
        return this.world.GetBodyList()
    }

    createBox(x, y, width, height, r, fixed, density) {
        if (r == 0 || r == undefined) {
            var vtx = [ {'x':-width/2, 'y':-height/2},
                {'x':width/2, 'y':-height/2},
                {'x':width/2, 'y':height/2},
                {'x':-width/2, 'y':height/2}]
            return this.createPolygon(x+(width/2),y+(height/2), vtx, fixed, density)
        } else {
            var cosr = cos(r), sinr = sin(r)
            var dx = width/2, dy = height/2
            var vtx = [ {'x':-dx*cosr+dy*sinr, 'y':-dx*sinr-dy*cosr},
                {'x':dx*cosr+dy*sinr, 'y':dx*sinr-dy*cosr},
                {'x':dx*cosr-dy*sinr, 'y':dx*sinr+dy*cosr},
                {'x':-dx*cosr-dy*sinr, 'y':-dx*sinr+dy*cosr}]
            return this.createPolygon(x+(width/2),y+(height/2), vtx, fixed, density)
        }
    }
}