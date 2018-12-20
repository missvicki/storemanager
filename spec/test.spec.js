var forlogin = require('../UI/scripts/login')
describe('login test', () => {
    let  user;

    beforeEach(() => {
        user = {
            user_name: "vickib",
            password: "vibel",
            role: "admin"
        };
    });
    
    it("should login a registered user", () => {
        expect(user.user_name).not.toBeNull;
        expect(user.password).not.toBeNull;
        expect(user.role).not.toBeNull;
        
        const data = {access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1N…NzIn0.Hoqwudkrg1YpPkDeoxweGUBFCueGbPAAMPQ-a1t0c_U"}
        spyOn(index, forlogin.login).and.returnValue(Promise.resolve(data))

        forlogin.login()
            .then((result) => {
            expect(result).toEqual(data)
            done();
        })
    });
})
