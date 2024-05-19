from csit314.app import db

class UserProfile(db.Model):
    __tablename__ = 'profile'
    profileName = db.Column(db.String(50), unique=True, primary_key=True)
    profileDescription = db.Column(db.String(50))
    status = db.Column(db.String(50))

    @classmethod
    def createUserProfile(cls, profileDetails: dict):
        profileName = cls.query.filter_by(profileName=profileDetails["profileName"]).one_or_none()
        if profileName:
            return False
        new_profile = cls(**profileDetails)
        db.session.add(new_profile)
        db.session.commit()
        return True

    @classmethod
    def profileNameExists(cls, profileDetails):
        return cls.query.filter_by(profileName=profileDetails["profileName"]).one_or_none()

    @classmethod
    def getAllProfiles(cls):
        return cls.query.all()

    @classmethod
    def getProfile(cls, profileName):
        return cls.query.filter_by(profileName=profileName).first()

    @classmethod
    def updateUserProfile(cls, profileName, updateDetails):
        profile = cls.getProfile(profileName)
        new_profileName = updateDetails.get('profileName')

        if new_profileName and new_profileName != profile.profileName:
            if cls.profileNameExists(updateDetails):
                return False

        profile.profileName = new_profileName or profile.profileName
        profile.profileDescription = updateDetails.get('profileDescription', profile.profileDescription)
        profile.status = updateDetails.get('status', profile.status)

        db.session.commit()
        return True

    @classmethod
    def search_profile(cls, searchQuery):
        profiles = cls.query.filter(cls.profileName.ilike(f'%{searchQuery}%')).all()
        if not profiles:
            return None
        return [profile.serialize() for profile in profiles]

    def serialize(self):
        return {
            'profileName': self.profileName,
            'profileDescription': self.profileDescription,
            'status': self.status
        }

    @classmethod
    def suspend_profile(cls, profileName):
        profile = cls.getProfile(profileName)
        if profile:
            if profile.status == 'Active':
                profile.status = 'Suspended'
                db.session.commit()
                return True
            else:
                return False
        return False
