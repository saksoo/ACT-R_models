import PySimpleGUI27 as sg
import params


# Initiation
activity = 0
CDR = 0

sg.change_look_and_feel('BlueMono')      # Add some color to the window

# Very basic window.  Return values using auto numbered keys

layout = [
    [sg.Text('Enter the parameters to run the models:', size=(25, 1))],
    [sg.Drop(values=('Tea Preparation Activity', 'Washing Hands Activity', 'Dressing Activity'), auto_size_text=True)], #0
    [sg.Drop(values=('MCI', 'Mild AD', 'Moderate AD', 'Severe AD'), auto_size_text=True)], #1
    [sg.Text('# People', size=(20, 1)), sg.InputText()], #2
    [sg.Text('Advanced parameters for the Declarative Memory Module:')],

    [sg.Text('Chunk Activation Transitory Noise e:', size=(25, 1)), sg.InputText()], #3
    [sg.Text('Strength of Association S:', size=(25, 1)), sg.InputText()],  # 4
    [sg.Text('Attentional Weight W:', size=(25, 1)), sg.InputText()], # 5
    [sg.Text('Strength of Similarity P:', size=(25, 1)), sg.InputText()], # 6
    [sg.Text('Similarity of Chunks:', size=(25, 1)), sg.InputText()], # 7
    [sg.Text('Advanced parameters for the Production Module:')], #
    [sg.Text('Production Utility Noise e:', size=(25, 1)), sg.InputText()], # 8
    [sg.Text('Production Utility Success:', size=(25, 1)), sg.InputText()], # 9
    [sg.Text('Production Utility Fail:', size=(25, 1)), sg.InputText()], # 10
    [sg.Text('Physical help factor:', size=(25, 1)), sg.InputText()], # 11
    [sg.Text('Verbal help factor:', size=(25, 1)), sg.InputText()], # 12
    [sg.Submit(button_text='Run'), sg.Cancel()] #
]

my_font = ("Arial", 13)
window = sg.Window('Simulation of daily activities', layout, element_justification='c', size=(700, 550), font=my_font)
event, values = window.read()
window.close()
print(event)


if values[0] == 'Tea Preparation Activity': activity = 1
if values[0] == 'Washing Hands Activity': activity = 2
if values[0] == 'Dressing Activity': activity = 3

if values[1] == 'MCI': CDR = 0.5
if values[1] == 'Mild AD': CDR = 1
if values[1] == 'Moderate AD': CDR = 2
if values[1] == 'Severe AD': CDR = 3


#adjust parameters

if CDR == 0:
    params.W = 3
    params.Ps = 0
    params.similarity = -1
    params.utility_success = 1
    params.utility_fail = 0
elif CDR == 0.5:  ## MCI
    params.W = 1.45
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.8
    params.utility_fail = 1 - params.utility_success
elif CDR == 1:  ## MILD AD
    params.W = 1.285
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.62
    params.utility_fail = 1 - params.utility_success
elif CDR == 2:  ## MODERATE AD
    params.W = 1.08
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.475
    params.utility_fail = 1 - params.utility_success
elif CDR == 3: ## SEVERE AD
    params.W = 1.035
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.3
    params.utility_fail = 1 - params.utility_success

if values[2]: params.N = int(values[2])
if values[3]: params.e_chunk_activation_transitory_noise = float(values[3])
if values[4]: params.S_chunk_strength_of_association = float(values[4])
if values[5]: params.W = float(values[5])
if values[6]: params.Ps = float(values[6])
if values[7]: params.similarity = float(values[7])
if values[8]: params.e_production_utility_transitory_noise = float(values[8])
if values[9]: params.utility_success = float(values[9])
if values[10]: params.utility_fail = float(values[10])
if values[11]: params.physical_factor = float(values[11])
if values[12]: params.verbal_factor = float(values[12])


if activity == 1:
    params.CDR = CDR

    print "Activity chosen: TEA PREPARATION"
    print "Level of AD: CDR-%.1f" % CDR
    print "Run for", params.N, "people."

    execfile('tea_experiment.py')

elif activity == 2:
    params.CDR = CDR

    print "Activity chosen: WASHING HANDS"
    print "Level of AD: CDR-%.1f" % CDR
    print "Run for", params.N, "people."

    execfile('washing_experiment.py')

elif activity == 3:
    params.CDR = CDR

    print "Activity chosen: DRESSING"
    print "Level of AD: CDR-%.1f" % CDR
    print "Run for", params.N, "people."

    execfile('dressing_experiment.py')
