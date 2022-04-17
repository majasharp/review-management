class User:
    def __init__(self, id, name, email, join_date, isTeamLeader=None):
        self.id = id
        self.first_name = name
        self.email = email
        self.join_date = join_date
        self.is_team_leader = None
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.first_name
    
    def get_email(self):
        return self.email
    
    def get_join_date(self):
        return self.join_date

    def get_is_team_leader(self):
        return self.is_team_leader

    def set_is_team_leader(self, is_tl):
        self.is_team_leader = is_tl