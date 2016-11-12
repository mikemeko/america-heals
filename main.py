import collections
import random

# Stance enumeration.
DEMOCRAT = 'DEMOCRAT'
REPUBLICAN = 'REPUBLICAN'
ANY = 'ANY'

STANCE_MATCHING = {
    DEMOCRAT: {DEMOCRAT},
    REPUBLICAN: {REPUBLICAN},
    ANY: {DEMOCRAT, REPUBLICAN, ANY},
}

# `email` can be used as ID.
User = collections.namedtuple(
    'User',
    ('name', 'age', 'email', 'stance', 'opposite_stance'))

def arg_max(items, f):
  max_item, max_value = None, None
  for item in items:
    value = f(item)
    if max_value is None or value > max_value:
      max_item, max_value = item, value
  return max_item

def match_score(user1, user2):
  if (user1.stance not in STANCE_MATCHING[user2.opposite_stance]
      or user2.stance not in STANCE_MATCHING[user1.opposite_stance]):
    return 0
  return 100 - abs(user1.age - user2.age)

def match(users):
  matched = set()
  pairs = []
  for user in users:
    if user in matched:
      continue
    matched.add(user)
    match = arg_max([u for u in users if u not in matched],
                    lambda u: match_score(user, u))
    if match is not None:
      matched.add(match)
      pairs.append((user, match))
  return pairs

def rand_user():
  name = 'slim jimmy'
  age = random.randint(18, 60)
  email = '%s@abc.com' % name
  stance = random.choice([DEMOCRAT, REPUBLICAN])
  opposite_stance = random.choice([DEMOCRAT, REPUBLICAN, ANY])
  return User(name=name,
              age=age,
              email=email,
              stance=stance,
              opposite_stance=opposite_stance)

if __name__ == '__main__':
  num_users = 10000 # 1000000 takes ~2.5 mins on Mac Air
  users = [rand_user() for _ in xrange(num_users)]
  pairs = match(users)
  if 0:
    for (user1, user2) in pairs:
      print ((user1.stance, user1.opposite_stance),
             (user2.stance, user2.opposite_stance))
  print '%d matches.' % len(pairs)
