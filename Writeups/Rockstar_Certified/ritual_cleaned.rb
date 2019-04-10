def void(something)
  """
  everything = 10000
  nothingness = nil
  while something != nothingness && nothingness < everything
    nothingness += 1
  end

  return nothingness
  """
  # above code makes nothingness == something
  # then returns nothingness
  return something
end

def the_earth(life, death)
  """
  until death > life
    life = life - death
  end
  return life
  """
  # above code calculates modulo: life % death
  return life % death
end

def his_reincarnation(my_soul, your_blood)
  """
  his_life = nil
  while my_soul >= your_blood
    my_soul = my_soul - your_blood
    his_life += 1
  end

  return his_life
  """
  # above code calculates integer division: my_soul / your_blood
  return (my_soul / your_blood).floor
end

print '> '
__input = $stdin.gets.chomp
@your_whispers = Float(__input) rescue __input
#@ice = void(my_soul)
@ice = @your_whispers

print '> '
__input = $stdin.gets.chomp
@your_screams = Float(__input) rescue __input
#@fire = void(@ice)
@fire = @your_screams

# Above code, input from user:
# ice = input_1
# fire = input_2
#################################

@energy = 2
@ashes = @energy - @energy
@potential = @energy / @energy

while @ice > 0 || @fire > 0
  @wind = the_earth(@ice, @energy) # modulo 2
  @earth = the_earth(@fire, @energy) # modulo 2
  @ice = his_reincarnation(@ice, @energy) # division 2
  @fire = his_reincarnation(@fire, @energy) # division 2
  if @wind > @earth || @earth > @wind # either-or but not both equal (XOR)
    @ashes = @ashes + @potential # @ashes+=1
  end

  @potential = @potential * @energy # multiply by 2
end

# Above code, while loop:
# count number of 1-bits of (both inputs XOR-ed together) -> ashes
# potential = 2**ashes
#################################

@his_heart = 12
@space = his_reincarnation(@ashes, @his_heart) # division 12
@flow = the_earth(@ashes, @his_heart) # modulo 12 
@time = "Mysterious "
if @flow == 1
  @time = "January "
end

if @flow == 2
  @time = "February "
end

if @flow == 3
  @time = "March "
end

if @flow == 4
  @time = "April "
end

if @flow == 5
  @time = "May "
end

if @flow == 6
  @time = "June "
end

if @flow == 7
  @time = "July "
end

if @flow == 8
  @time = "August "
end

if @flow == 9
  @time = "September "
end

if @flow == 10
  @time = "October "
end

if @flow == 11
  @time = "November "
end

if @flow == 12
  @time = "December "
end

puts (@time + @space.to_s).to_s

