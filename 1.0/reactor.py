from itertools import permutations 


class Reactor:
  def __init__(self, name, MW,NOIR , permutations_list):
    self.name = name
    self.MW = MW
    self.NOIR = NOIR
    self.permutations_list = permutations_list
  def generate_all_permutations(self , timePeriod : int):
    loop2 = timePeriod - int(self.NOIR)+1
    if int(self.NOIR) == 0 :
      loop1 = 1
    else:
      loop1 = loop2
    i =0
    while i  < loop1:
      j=0
      item = []
      while j < loop2:
        if i == j :
          for k in range(int(self.NOIR)):
            item.append(1)
        else :
          item.append(0)
        j+=1
      self.permutations_list.append(item)
      i+=1 
    
    # first_state = []
    # NOIR = int(self.NOIR)
    # for i in range(timePeriod):
    #   if i < NOIR :
    #     first_state.append(1)
    #   else:
    #     first_state.append(0)
    # perm = permutations(first_state)
    # all_perm = [] 
    # for i in list(perm):
    #   all_perm.append(i)
    # all_perm = list(dict.fromkeys(all_perm))
    # acceptable = True
    # for item in all_perm:
    #   seeOne = False
    #   seeZeroAfterOne = False
    #   acceptable = True
    #   for i in item:
    #     if( seeOne == False and i == 1):
    #       seeOne = True
    #     elif seeOne == True and i == 0 :
    #       seeZeroAfterOne = True
    #     elif seeZeroAfterOne == True and i==1 :
    #       acceptable = False 
    #   if acceptable :
    #     self.permutations_list.append(item)

