# adsrex

Collection of functional tests for ADS Api and Bumblebee.

A minimal configuration is necessary, create a `local_config.py`
and set the values as described in the `config.py`

The tests have to be *self-contained*, i.e. v1_0 should not 
share any code with v1_1!

*These tests are python 3.x!*

## How to write new tests

There are 3 use types:

    - anonymous_user: will make requests to the API without any token
    - bumblebee_user: will make requests to the API as short-lived BBB (anonymous) user
    - authenticated_user: special account `tester@ads` represents a logged-in, authenticated user; this account has very high ratelimits everything else (permissions) is the same as standard users
    
Tests are organized per module/microservice. Each should exercise these 3 user categories. Typically, for authenticated/bumblebee user you can just write one test and pass in the user object, i.e.


```
def test(user=authenticated_user):
    r = user.get('/some/url', ....)
    assert r.status_code == 200
```


# usage

```py.test v1_0```

