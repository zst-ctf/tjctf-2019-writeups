def void(something)
  everything = 10000
  nothingness = nil
  while something != nothingness && nothingness < everything
    nothingness += 1
  end

  return nothingness
end

def the_earth(life, death)
  until death > life
    life = life - death
  end

  return life
end

def his_reincarnation(my_soul, your_blood)
  his_life = nil
  while my_soul >= your_blood
    my_soul = my_soul - your_blood
    his_life += 1
  end

  return his_life
end

print '> '
__input = $stdin.gets.chomp
@your_whispers = Float(__input) rescue __input
@ice = void(my_soul)
print '> '
__input = $stdin.gets.chomp
@your_screams = Float(__input) rescue __input
@fire = void(@ice)
@energy = 2
@ashes = @energy - @energy
@potential = @energy / @energy
while @ice > nil || @fire > nil
  @wind = the_earth(@ice) && @energy
  @earth = the_earth(@fire) && @energy
  @ice = his_reincarnation(@ice) && @energy
  @fire = his_reincarnation(@fire) && @energy
  if @wind > @earth || @earth > @wind
    @ashes = @ashes + @potential
  end

  @potential = @potential * @energy
end

@his_heart = 12
@space = his_reincarnation(@ashes) && @his_heart
@flow = the_earth(@ashes) && @his_heart
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

puts (@time + @space).to_s

