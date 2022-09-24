import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    '''
    Extending the BaseUserManager.
    '''
    def create_user(self, email, username, password=None):
        '''
        OverWriting the create_user function.
        '''
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        '''
        OverWriting the create_superuser function.
        '''

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    Creating thr custom user module schema.
    '''
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    is_a_supervisor         = models.BooleanField(default=False)
    first_name              = models.CharField(max_length=15, blank=True, null=True)
    last_name               = models.CharField(max_length=15, blank=True, null=True)
    employee_id             = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        '''
        Return the username as string
        '''
        return self.username

    def has_perm(self, perm, obj=None):
        '''
        For checking permissions. to keep it simple all admin have ALL permissons.
        '''
        return self.is_admin

    def has_module_perms(self, app_label):
        '''
        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
        '''
        return True




class Applicant(models.Model):
    '''
    Creating the applicant model and schema.
    '''

    # Creating a tuple to facilitate choices for applicantion status.
    # There are three states. accpeted if accepted; rejected if rejected; pending if the application has not reviewed. 
    STATUS = (
        ("0", 'Rejected'),
        ("1", 'Accepted'),
        ("2", 'Pending'),
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50,blank= True,null = True)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(blank=True,null = True)# made this optional for now
    resume = models.FileField(upload_to='uploads/resume/')
    cover_letter = models.FileField(upload_to='uploads/cover_letter/', blank=True, null=True)
    uid = models.IntegerField(null= True, blank=True, unique=True)
    slug = models.SlugField(null= True, blank=True, unique=True) # ths feel redudndant at the moment but have left it in here for now
    app_enum_status = models.CharField(max_length=10, choices=STATUS, default="2") # Source of truth for the application status
    app_status = models.BooleanField(blank=True,null=True) # this is just a reflection of the enum but cannot server as a source of truth for the application status

    class Meta:
        '''
        Editing some meta data od the model.
        '''
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
    
    ## This function has been commented out. 
    #if the user case was broder, then this function would be really help full to navigate a list full of applicants
    # def get_profile_url(self): 
    #     return f'http://127.0.0.1:8000/api/applicant/detail/{self.slug}'
        
    def get_resume(self):
        '''
        Creating a function to get the resume directly
        '''
        if self.resume:
            return 'http://127.0.0.1:8000'+self.resume.url
        return ''

    def get_cover_letter(self):
        '''
        Creating a function to get the cover letter directly
        '''
        if self.cover_letter:
            return 'http://127.0.0.1:8000'+self.cover_letter.url
        return ''


    def __str__(self):
        return str(self.uid)

    def create_uid(self):
        '''
        Generating a unique uid for every applicant
        '''
        not_a_unique_hash = True
        while not_a_unique_hash: # while True
            uid = int(''.join(str(random.randint(10, 99)))+''.join(str(random.randint(100, 999))))
            not_a_unique_hash = Applicant.objects.filter(uid=uid).exists()
        return uid

    
    def gen_uid_and_slug(self):
        uid = self.create_uid()
        self.uid = self.slug = uid
        self.save()

    def check_app_status_bool(self):
        '''
        Updating bool_status if app_enum_status is updated
        '''
        hashmap = {
            "0": False,
            "1": True,
            "2": None,
        }
        self.app_status=hashmap[self.app_enum_status]
        self.save()