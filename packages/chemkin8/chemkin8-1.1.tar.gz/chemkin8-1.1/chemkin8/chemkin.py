import numpy as np
import sqlite3
import os
from chemkin8.parser import *
from parser import * # to be deleted
import datetime
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


class backward:
    """Methods for calculating the backward reaction rate.

    Cp_over_R: Returns specific heat of each specie given by
               the NASA polynomials.
    H_over_RT:  Returns the enthalpy of each specie given by
                the NASA polynomials.
    S_over_R: Returns the entropy of each specie given by
              the NASA polynomials.
    backward_coeffs:  Returns the backward reaction rate
                      coefficient for reach reaction.
    """

    def __init__(self, nuij, nasa7_coeffs):
        self.nuij = np.array(nuij)
        self.nasa7_coeffs = np.array(nasa7_coeffs)
        self.p0 = 1.0e+05 # Pa
        self.R = 8.3144598 # J / mol / K
        self.gamma = np.sum(self.nuij, axis=1)

    def Cp_over_R(self, T):
        """Returns specific heat of each specie given by the NASA polynomials.

        INPUTS
        =======
        T: float, environment temperature

        RETURNS
        =======
        Cp_R: array of float, specific heat of each specie given by the NASA polynomials

        EXAMPLES
        ========
        >>> b = backward([[1,1]], [[1,1,1,1,1,1,1]])
        >>> b.Cp_over_R(200)
        array([  1.60804020e+09])
        """

        a = self.nasa7_coeffs

        Cp_R = (a[:,0] + a[:,1] * T + a[:,2] * T**2.0
                + a[:,3] * T**3.0 + a[:,4] * T**4.0)

        return Cp_R

    def H_over_RT(self, T):
        """Returns the enthalpy of each specie given by the NASA polynomials.

        INPUTS
        =======
        T: float, environment temperature

        RETURNS
        =======
        H_over_RT: array of float, the enthalpy of each specie given by the NASA polynomials

        EXAMPLES
        ========
        >>> b = backward([[1,1]], [[1,1,1,1,1,1,1]])
        >>> b.H_over_RT(200)
        array([  3.22013434e+08])
        """

        a = self.nasa7_coeffs

        H_RT = (a[:,0] + a[:,1] * T / 2.0 + a[:,2] * T**2.0 / 3.0
                + a[:,3] * T**3.0 / 4.0 + a[:,4] * T**4.0 / 5.0
                + a[:,5] / T)

        return H_RT

    def S_over_R(self, T):
        """Returns the entropy of each specie given by the NASA polynomials.

        INPUTS
        =======
        T: float, environment temperature

        RETURNS
        =======
        S_over_R: array of float, the entropy of each specie given by the NASA polynomials

        EXAMPLES
        ========
        >>> b = backward([[1,1]], [[1,1,1,1,1,1,1]])
        >>> b.S_over_R(200)
        array([  4.02686873e+08])
        """

        a = self.nasa7_coeffs

        S_R = (a[:,0] * np.log(T) + a[:,1] * T + a[:,2] * T**2.0 / 2.0
               + a[:,3] * T**3.0 / 3.0 + a[:,4] * T**4.0 / 4.0 + a[:,6])

        return S_R

    def backward_coeffs(self, kf, T):
        """Returns the backward reaction rate coefficient for reach reaction.

        INPUTS
        =======
        kf: array of float, forward reaction rate coefficients for each reaction
        T: float, environment temperature

        RETURNS
        =======
        kb: array of float, backward reaction rate coefficients for each reaction

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_reversible.xml')
        >>> c = chemkin(fname)
        >>> c.parseNASA(1500)
        >>> c.k_system(1500)
        >>> b = backward(c.v2 - c.v1, c.nasa)
        >>> b.backward_coeffs(c.kf, 1500)
        array([  7.86833492e+14,   8.03264045e+12,   2.92668218e+11,
                 8.02082564e+13,   3.94788406e+05,   2.48917653e+07,
                 7.15609711e+05,   2.18068945e+04,   2.43077455e+02,
                 3.43831179e+10,   1.82793668e+10])

        """

        # Change in enthalpy and entropy for each reaction
        delta_H_over_RT = np.dot(self.nuij, self.H_over_RT(T))
        delta_S_over_R = np.dot(self.nuij, self.S_over_R(T))

        # Negative of change in Gibbs free energy for each reaction
        delta_G_over_RT = delta_S_over_R - delta_H_over_RT

        # Prefactor in Ke
        fact = self.p0 / self.R / T

        # Ke
        kb = fact**self.gamma * np.exp(delta_G_over_RT)

        return kf / kb



class visualisations:
    """Methods for visualising nuclear reactions.

    draw_decay_graph: Generates plot for the decay of reactant
                      in a nuclear reaction.
    draw_decay_series:  Generates plot for the multi-step decay
                        of a radioactive element into a stable
                        isotope.
    """

    def __init__(self, path):
        self.dir_path = path

    def draw_decay_graph(self, halfLife, ele):
        """Generates plot for the decay of reactant in a nuclear reaction.

        INPUTS
        =======
        halfLife: float, time (in minutes) taken for reactant to reduce to
                  half its concentration.
        ele: string, name of the decaying isotope of the reactant.

        RETURNS
        =======
        The plot is saved in the outputs directory of the package, marked
        by the date and time of processing.

        EXAMPLES
        ========
        >>> output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> v = visualisations(output_dir)
        >>> v.draw_decay_graph(2.99592e-9, 'C-14')
        """

        k = np.log(2)/halfLife
        ts = np.linspace(0,10*halfLife,1001)
        As = [np.exp(-k*t) for t in ts]

        plt.plot(ts, As)
        plt.ylabel('Fraction of initial Concentration')
        plt.xlabel('Time (mins)')
        plt.title('Decay graph for %s, k = %e' %(ele,k))

        plt.xlim(0,10*halfLife)
        plt.ylim(0,1)
        plt.savefig(self.dir_path+ele+'.png')
        return


    def draw_decay_series(self, steps, name):
        """Generates plot for the multi-step decay of a radioactive element
        into a stable isotope.

        INPUTS
        =======
        steps: array of 3 lists
               First list contains names of products at each step.
               Second list contains atomic number of products at each step.
               Third list contains atomic number of products at each step.
        name: string, name of the decaying radioactive isotope.

        RETURNS
        =======
        The plot is saved in the outputs directory of the package, marked
        by the date and time of processing.

        EXAMPLES
        ========
        >>> output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> v = visualisations(output_dir)
        >>> steps = [['Rn', 'Po', 'Pb', 'Bi', 'Po', 'Pb', 'Bi', 'Po', 'Pb'], [86, 84, 82, 83, 84, 82, 83, 84, 82], [222, 218, 214, 214, 214, 210, 210, 210, 206]]
        >>> v.draw_decay_series(steps, 'Rn-222')
        """

        ele, Zs, As = steps[0], steps[1], steps[2]

        plt.scatter(Zs, As, color='k')
        for i in range(len(Zs)-1):
            if Zs[i+1]-Zs[i]<0: # alpha decay
                plt.arrow(Zs[i], As[i], Zs[i+1]-Zs[i]+0.02, As[i+1]-As[i]+0.02, color='#FFAF0D', head_width=0.3, head_length=0.2, length_includes_head=True)
            else: # beta decay
                plt.arrow(Zs[i], As[i], Zs[i+1]-Zs[i]-0.02, As[i+1]-As[i], color='#C20B59', head_width=0.3, head_length=0.2,  length_includes_head=True)

        plt.xlabel('Number of protons, Z')
        plt.ylabel('Mass Number, A')
        plt.xlim(Zs[-1]-4, Zs[0]+4)
        plt.ylim(As[-1]-4, As[0]+4)

        ele_dict = {}
        for i in np.arange(Zs[-1]-4, Zs[0]+4): ele_dict[i] = ''
        for i in range(len(Zs)): ele_dict[Zs[i]] = ele[i]

        labels = []
        for i in np.arange(Zs[-1]-4, Zs[0]+4):
            if ele_dict[i]=='': labels.append(str(i))
            else: labels.append(str(i)+'\n'+ele_dict[i])

        plt.xticks(np.arange(Zs[-1]-4, Zs[0]+4), labels)
        plt.yticks(np.arange(As[-1]-4, As[0]+5, 2))

        plt.title('Decay series for '+name)

        plt.plot([0,0], [0.5,0.6], color='#FFAF0D', label='Alpha Decay'),
        plt.plot([1,1], [1.5,1.6], color='#C20B59', label='Beta Decay')
        plt.legend()

        plt.tight_layout()
        plt.savefig(self.dir_path + name + '.png')
        plt.gcf().clear()
        return None


# Adding a new class for nuclear reactions_dict
class nuclear:
    """Methods for completing nuclear reactions

    parse: Parses file containing nuclear reactions and stores it in internal
           array.
    print_reaction:  Prints complete set of reaction(s) to file and on console.
    check_stable: Checks if reaction products are stable or decay further
    reaction_string: Generates complete individual reactions.
    find_reaction_type: Detects the type of reaction occuring out of 6 kinds
    generate_decay_series:  Generates the decay sequence for an unstable
                            radioactive product
    """

    def __init__(self, file):
        self.reactions = []
        self.file = os.path.dirname(os.path.realpath(__file__))
        self.parse(file)


    def parse(self, file):
        """Parses file containing nuclear reactions and stores it in internal
        array.

        INPUTS
        =======
        file: string, name of xml file containing data about nuclear reactions.

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_nuclear.xml')
        >>> n = nuclear(fname)
        >>> n.reactions[0]['products']
        ['Rn']
        """
        self.reactions = parseNuclearXML(file)


    def print_reaction(self, verbose = True, visualise = True):
        """Prints complete set of reaction(s) to file and on console.

        INPUTS
        =======
        verbose: boolean value, specifies if reaction details should be printed
                 as console output or not.
        visualise: boolean value, specifies if reactant decay plots should be
                   generated or not.


        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_nuclear.xml')
        >>> n = nuclear(fname)
        >>> n.print_reaction(verbose=True).split('\\n')[:2]
        ['================= Reaction 1 =================', 'Alpha Decay: Ra(88, 226) --> Rn(86, 222)']
        """

        db, self.cursor = None, None
        try:
            db = sqlite3.connect(self.file + '/nucleardb.sqlite')
            self.cursor = db.cursor()
        except:
            raise ValueError('Database not connected!')

        now = datetime.datetime.now()
        dir_path = "outputs/"+now.isoformat()+"/"
        file_path = dir_path+"reac_output.txt"

        v = None
        if visualise:
            v = visualisations(dir_path)
            if not os.path.exists(dir_path):
                os.makedirs(os.path.dirname(dir_path))

        reac_str = ''
        # Assessing if decay series required
        for i, reaction in enumerate(self.reactions):
            if i > 0: reac_str += '\n\n'
            reac_str += '================= Reaction %d =================\n'%(i+1)
            reac_str += self.find_reaction_type(reaction)     # Find reaction type of original reaction
            for i,p in enumerate(reaction['products']):
                query = '''SELECT STABLE from ELEMENT_PROPERTIES WHERE SYMBOL='%s' and ATOMIC_WEIGHT=%d''' %(p, reaction['p_mass'][i])
                status = self.cursor.execute(query).fetchall()[0][0] # Find status of each product(stable/unstable)
                if status=='NO':          # Print decay steps of product
                    reac_str += '\n\tProducts not stable. Further reactions initiated.\n'
                    # ele_arr = [[reaction['reactants'][0]]] - Add starting element maybe @MSR
                    name = reaction['reactants'][0]+'-'+str(int(reaction['r_mass'][0]))
                    reac_str += self.generate_decay_series(reaction['products'][i], reaction['p_mass'][i], v, name)
                else:
                    reac_str += '\nProducts stable. No further reactions.'
                    if visualise:
                        name = reaction['reactants'][0]+'-'+str(int(reaction['r_mass'][0]))
                        v.draw_decay_graph(reaction['halfLife'], name)

        reac_output = open(file_path, "w")
        reac_output.write(reac_str)
        reac_output.close()

        if verbose:
            return reac_str
        else:
            return


    def reaction_string(self, r, p, n1, n2, v1, v2, reac_type):  # n1, n2 are atomic numbers
        """Generates complete individual reactions.

        INPUTS
        =======
        r: array of strings, symbol of each reactant
        p: array of strings, symbol of each product
        n1: array of float, atomic number of each reactant
        n2: array of float, atomic number of each product
        v1: array of float, atomic weight of each reactant
        v2: array of float, atomic weight of each product
        reac_type: array of string, nature of each nuclear reaction

        RETURNS
        =======
        reac_str: string, complete reaction with reaction type

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_nuclear.xml')
        >>> n = nuclear(fname)
        >>> n.reaction_string(['U'], ['Th', 'alpha'], [92], [90, 2], [238], [234, 4], 'Alpha Decay')
        'Alpha Decay: U(92, 238) --> Th(90, 234) + alpha(90, 234)'
        """

        reac_str = "%s: %s(%s, %d)" %(reac_type, r[0], n1[0], v1[0])

        for i, each_r in enumerate(r[1:]):
            reac_str += '+ %s(%s, %d)'%(each_r, n1[i], v1[i])

        reac_str += ' --> %s(%s, %d)'%(p[0], n2[0], v2[0])

        for i, each_p in enumerate(p[1:]):
            reac_str += ' + %s(%s, %d)'%(each_p, n2[i], v2[i])

        return reac_str


    def find_reaction_type(self, reaction):
        """Detects the type of reaction occuring out of 6 kinds
            a. Alpha Decay
            b. Beta Decay
            c. Positron Emission
            d. Electron Capture
            e. Gamma Emission
            f. Spontaneous Fission

        INPUTS
        =======
        reaction: dictionary of values, containing details of a reactions

        RETURNS
        =======
        reac_str: Returns string form of given reaction

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_nuclear.xml')
        >>> n = nuclear(fname)
        >>> db = sqlite3.connect(n.file + '/nucleardb.sqlite')
        >>> n.cursor = db.cursor()
        >>> reaction = {'id': 'reaction01', 'reactants': ['Ra'], 'r_mass': [226.0], 'products': ['Rn'], 'p_mass': [222.0], 'halfLife': 840960000.0}
        >>> n.find_reaction_type(reaction)
        'Alpha Decay: Ra(88, 226) --> Rn(86, 222)'
        """

        z1, z2 = [], []
        for r in reaction['reactants']:
            try:
                z1.append(self.cursor.execute('''SELECT ATOMIC_NUMBER FROM ELEMENT_PROPERTIES WHERE SYMBOL = "%s"'''%r.strip('*')).fetchall()[0][0])
            except:
                z1.append('nan')
        for p in reaction['products']:
            try:
                z2.append(self.cursor.execute('''SELECT ATOMIC_NUMBER FROM ELEMENT_PROPERTIES WHERE SYMBOL = "%s"'''%p.strip('*')).fetchall()[0][0])
            except:
                z2.append('nan')

        if len(reaction['products']) == 2:
            if 'Xray' in reaction['products']:
                reac_type = 'Electron Capture'
            else:
                reac_type = 'Spontaneous Fission'
        else:
            if reaction['reactants'][0].strip('*') == reaction['products'][0]:
                reac_type = 'Gamma Emission'
            elif reaction['r_mass'][0] - reaction['p_mass'][0] == 4:
                reac_type = 'Alpha Decay'
            else:
                if int(z1[0]) == int(z2[0]) - 1:
                    reac_type = 'Beta Decay'
                elif int(z1[0]) == int(z2[0]) + 1:
                    reac_type = 'Positron Emission'
                else:
                    raise ValueError('No reaction type found. Please check your XML.')

        # Printing reaction
        reac_str = self.reaction_string(reaction['reactants'], reaction['products'], z1, z2, reaction['r_mass'], reaction['p_mass'], reac_type)
        return reac_str


    def generate_decay_series(self, p = None, v2 = None, vizObj = None, name = None):
        """Prints radiactive decay series of element

        INPUTS
        =======
        p: single string, symbol of radioactive element
        v2: single float value, atomic weight of radioactive element
        vizObj = object of visualisations class, if not None then plot of
                 radioactive decay should be generated
        name = string, name of radioactive isotope that is decaying further

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_nuclear.xml')
        >>> n = nuclear(fname)
        >>> n.generate_decay_series(n.reactions[1]['products'][0], n.reactions[1]['p_mass'][0])
        'Further reaction: Decay of N-14\\nFurther reaction not recorded'
        """
        # Connect to DB
        db = sqlite3.connect(self.file + '/nucleardb.sqlite')
        cursor = db.cursor()

        # Print series of reactions
        if name == None: name = self.reactions[0]['reactants'][0]+'-'+str(int(self.reactions[0]['r_mass'][0]))
        if p == None: p = self.reactions[0]['products'][0]
        if v2 == None: v2 = self.reactions[0]['p_mass'][0]


        prev_step, status = 'alpha', 'NO'
        cur_r, at_wt = p, v2
        at_num = int(cursor.execute('''SELECT ATOMIC_NUMBER from ELEMENT_PROPERTIES WHERE SYMBOL='%s' and ATOMIC_WEIGHT=%d''' %(p, at_wt)).fetchall()[0][0])

        decay_str = 'Further reaction: Decay of %s-%d' %(p,v2)

        if vizObj != None:
            decay_steps = [[cur_r], [at_num], [int(at_wt)]]

        while status == 'NO':
            cur_step, cur_p = None, None

            # 1. Find alpha and beta decay products
            query = '''SELECT * from ELEMENT_PROPERTIES WHERE ATOMIC_NUMBER='%d' and ATOMIC_WEIGHT=%d'''
            try:
                alpha = cursor.execute(query %(at_num-2, at_wt-4)).fetchall()[0]
            except:
                alpha = None

            try:
                beta = cursor.execute(query %(at_num+1, at_wt)).fetchall()[0]
            except:
                beta = None

            # 2. Check if reaction exists
            if alpha == None and beta == None:
                decay_str += '\nFurther reaction not recorded'
                vizObj = None
                break

            # 3. If any one step makes it stable, select that
            if alpha!=None and beta!=None:
                if alpha[4]=='YES' and beta[4]!='YES': cur_step='alpha'
                elif beta[4]=='YES' and alpha[4]!='YES': cur_step='beta'

            # 4. If both make it stable or only one further step, find next reaction step, preferably one that ensures balanced decline (alternate alpha, beta)
            if cur_step == None:
                if prev_step == 'alpha':
                    if beta!=None: cur_step = 'beta'
                    else: cur_step = 'alpha'
                elif prev_step == 'beta':
                    if alpha!=None: cur_step = 'alpha'
                    else: cur_step = 'beta'

            # 5. Print step and reset variables for next step
            if cur_step=='alpha':
                decay_str += '\n\t%s'%self.reaction_string([cur_r], [alpha[0]], [at_num], [int(alpha[2])], [at_wt], [float(alpha[3])], 'Alpha Decay')
                cur_p, status = alpha[0], alpha[4]
                at_num, at_wt = at_num-2, at_wt-4
            elif cur_step=='beta':
                decay_str += '\n\t%s'%self.reaction_string([cur_r], [beta[0]], [at_num], [int(beta[2])], [at_wt], [float(beta[3])], 'Beta Decay')
                cur_p, status = beta[0], beta[4]
                at_num += 1
            prev_step, cur_r = cur_step, cur_p

            if vizObj!=None:
                decay_steps[0].append(cur_p)
                decay_steps[1].append(at_num)
                decay_steps[2].append(int(at_wt))

        if vizObj!=None:
            vizObj.draw_decay_series(decay_steps, name)
        return decay_str


class chemkin:
    def __init__(self, file):
        self.r = 8.314
        self.v1 = None
        self.v2 = None
        self.rates = None
        self.kf = None
        self.kb = None
        self.reversible = None
        self.nasa = []
        self.file = os.path.dirname(os.path.realpath(__file__))
        self.parse(file)

    def parse(self, file):
        """Calls parser and stores instance attributes

        INPUTS
        =======
        file: string, path of XML file to be parsed

        RETURNS
        =======
        None. Instance attributes added:
        rates: dictionary of reaction rate coefficients information
               need to call reaction_rate() to calculate list k
        v1: coefficients of reactants
        v2: coefficients of products

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> c = chemkin(fname)
        >>> c.v1
        array([[ 1.,  0.,  0.,  0.,  0.,  1.],
               [ 0.,  1.,  0.,  1.,  0.,  0.],
               [ 0.,  0.,  1.,  1.,  0.,  0.]])
        """
        self.species_lst, reactions_dict, self.reversible = parseXML(file)
        self.rates = reactions_dict['rates']

        self.v1 = []
        self.v2 = []
        for species in self.species_lst:
            self.v1.append(reactions_dict['reactants'][species])
        for species in self.species_lst:
            self.v2.append(reactions_dict['products'][species])


        self.v1 = np.array(self.v1).T
        self.v2 = np.array(self.v2).T

    def parseNASA(self, T, feed=None):
        """Reads the NASA polynomials from the database nasapoly.sqlite and stores them in self.nasa

        INPUTS
        =======
        T: float, environment temperature
        feed: optional, polynomials to be directly passed to self.nasa

        RETURNS
        =======
        None. Modifies self.nasa.

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns_reversible.xml')
        >>> c = chemkin(fname)
        >>> c.parseNASA(1500)
        >>> c.nasa
        [(2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.446682914), (2.56942078, -8.59741137e-05, 4.19484589e-08, -1.00177799e-11, 1.22833691e-15, 29217.5791, 4.78433864), (3.09288767, 0.000548429716, 1.26505228e-07, -8.79461556e-11, 1.17412376e-14, 3858.657, 4.4766961), (3.3372792, -4.94024731e-05, 4.99456778e-07, -1.79566394e-10, 2.00255376e-14, -950.158922, -3.20502331), (3.03399249, 0.00217691804, -1.64072518e-07, -9.7041987e-11, 1.68200992e-14, -30004.2971, 4.9667701), (3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129), (4.0172109, 0.00223982013, -6.3365815e-07, 1.1424637e-10, -1.07908535e-14, 111.856713, 3.78510215), (4.16500285, 0.00490831694, -1.90139225e-06, 3.71185986e-10, -2.87908305e-14, -17861.7877, 2.91615662)]

        """
        if feed is None:
            db = sqlite3.connect(self.file + '/nasapoly.sqlite')
            cursor = db.cursor()
            low = {i[0]: i for i in cursor.execute('''SELECT * FROM LOW''').fetchall()}
            high = {i[0]: i for i in cursor.execute('''SELECT * FROM HIGH''').fetchall()}
            for i in self.species_lst:
                if T <= low[i][2]:
                    self.nasa.append(low[i][3:])
                else:
                    self.nasa.append(high[i][3:])
        else:
            self.nasa = feed

    def NASAcoeffs(self):
        """Returns NASA coeffs

        INPUTS
        =======
        None

        RETURNS
        =======
        self.nasa: numpy array, nasa coefficients

        EXAMPLES
        =======
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> c = chemkin(fname)
        >>> c.parseNASA(1500)
        >>> c.NASAcoeffs()
        [(2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.446682914), (2.56942078, -8.59741137e-05, 4.19484589e-08, -1.00177799e-11, 1.22833691e-15, 29217.5791, 4.78433864), (3.09288767, 0.000548429716, 1.26505228e-07, -8.79461556e-11, 1.17412376e-14, 3858.657, 4.4766961), (3.3372792, -4.94024731e-05, 4.99456778e-07, -1.79566394e-10, 2.00255376e-14, -950.158922, -3.20502331), (3.03399249, 0.00217691804, -1.64072518e-07, -9.7041987e-11, 1.68200992e-14, -30004.2971, 4.9667701), (3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129)]
        """
        return self.nasa

    def k_constant(self, k):
        """Returns the constant reaction rate coefficient.

        INPUTS
        =======
        k: int or float, the constant reaction rate coefficient

        RETURNS
        ========
        k: float, the constant reaction rate coefficient

        EXAMPLES
        =========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> chemkin(fname).k_constant(10.0)
        10.0
        """
        try:
            k = float(k)
        except:
            raise TypeError("Error: unable to convert k to float!")
        return k

    def k_arrhenius(self, a, e, t):
        """Returns the Arrhenius reaction rate coefficient.

        INPUTS
        =======
        a: int or float, Arrhenius prefactor, A, is strictly positive
        e: int or float, the activation energy for the reaction
        t: int or float, the temperature T, must be positive (assuming a Kelvin scale)

        RETURNS
        ========
        k: float, the Arrhenius reaction rate coefficient

        EXAMPLES
        =========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> chemkin(fname).k_arrhenius(10,10,10)
        8.8667297841210573
        """
        try:
            a = float(a)
            e = float(e)
            t = float(t)
        except:
            raise ValueError("Error: unable to convert all parameters to float!")
        if a <= 0:
            raise ValueError("The Arrhenius prefactor A must be positive")
        if t <= 0:
            raise ValueError("The temperature T must be positive (assume a Kelvin scale)")
        return a*np.exp(-e/(self.r*t))

    def k_modified(self, a, b, e, t):
        """Returns the modified Arrhenius reaction rate coefficient.

        INPUTS
        =======
        a: int or float, Arrhenius prefactor, A, is strictly positive
        b: int or float, fitted rate constant
        e: int or float, the activation energy for the reaction
        t: int or float, the temperature T, must be positive (assuming a Kelvin scale)

        RETURNS
        ========
        k: float, the modified Arrhenius reaction rate coefficient

        EXAMPLES
        =========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> chemkin(fname).k_modified(10**7,0.5,10**3,10**2)
        30035490.889639609
        """
        if isinstance(b, complex):
            raise ValueError("The modified Arrhenius parameter b must be real")
        try:
            a = float(a)
            b = float(b)
            e = float(e)
            t = float(t)
        except:
            raise ValueError("Error: unable to convert all parameters to float!")
        if a <= 0:
            raise ValueError("The Arrhenius prefactor A must be positive")
        if t <= 0:
            raise ValueError("The temperature T must be positive (assume a Kelvin scale)")
        return a*(t**b)*np.exp(-e/(self.r*t))

    def k_system(self, T):
        """Calculates a list of k, one for each reaction.

        INPUTS
        =======
        rates: dictionary containing reaction rate type and all parameters pertaining to set of reactions
        T: int or float, environment temperature

        RETURNS
        =======
        None. Class attributes are added:
        k: list of floats, has length m where m is the number of reactions

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> c = chemkin(fname)
        >>> c.k_system(1500)
        >>> c.kf
        [114837571.22536749, 2310555.9199959813, 1000.0]
        """
        if self.rates is None:
            raise ValueError("Rates not initialized. Please call Chemkin().parse() to parse XML first.")

        self.kf = []
        for reaction in self.rates:
            if reaction['type'] == 'Arrhenius':
                self.kf.append(self.k_arrhenius(reaction['A'], reaction['E'], T))
            elif reaction['type'] == 'modifiedArrhenius':
                self.kf.append(self.k_modified(reaction['A'], reaction['b'], reaction['E'], T))
            elif reaction['type'] == 'Constant':
                self.kf.append(self.k_constant(reaction['k']))

    def progress_reaction(self, x, kf, v1, kb=None, v2=None):
        """Returns the progress rate of a single reaction.

        INPUTS
        =======
        x: list of concentration of each species
        kf: int or float, the reaction rate coefficient
        v: list of Stoichiometric coefficients of reactants

        RETURNS
        ========
        progress rate: float, the progress rate of a reaction

        EXAMPLES
        =========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> chemkin(fname).progress_reaction([1,2,3], 10, [2,1,0])
        20
        """
        if len(x) != len(v1):
            raise ValueError("Dimensions of concentration and coefficients do not match!")
        if kf==0:
            raise ValueError("Reaction rate of reaction is 0. No reaction.")
        if x==[0]*len(x):
            raise ValueError("All reactant concentrations for reaction are 0.")
        if list(v1)==[0]*len(v1):
            raise ValueError("All stoich coefficients for reaction are 0.")

        progress_f = kf
        for i in range(len(x)):
            progress_f = progress_f * (x[i]**v1[i])

        progress_b = 0
        if kb is not None and v2 is not None:
            progress_b = kb
            for i in range(len(x)):
                progress_b = progress_b * (x[i]**v2[i])

        return progress_f - progress_b

    def progress_system(self, x, T=None):
        """Returns the progress rate of a system of reactions.

        INPUTS
        =======
        x: list of concentration of each species

        RETURNS
        ========
        progress rate: list of progress rate of each reaction

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> c = chemkin(fname)
        >>> c.k_system(1500)
        >>> c.progress_system([2., 1., .5, 1., 1., 1.])
        [229675142.45073497, 2310555.9199959813, 500.0]
        """
        if self.kf is None:
            raise ValueError("Reaction rate coefficients not initialized. Please call Chemkin().k_system() to calculate list k first.")

        if len(self.v1) != len(self.kf):
            raise ValueError("Number of k does not much number of reactions!")

        for lst in self.v1:
            if any(isinstance(d, complex) for d in lst) == True:
                raise ValueError('Complex value in reactant coefficient detected!')

        progress = []
        for i in range(len(self.v1)):

            if len(self.v1[i]) != len(x):
                raise ValueError("Not enough coefficient values! Check the dimension of coefficient matrix.")

            if self.reversible[i] == 'yes':
                if self.nasa is None:
                    raise ValueError("NASA polynomials are not imported successfully. Please check your database.")
                bw = backward(self.v2 - self.v1, self.nasa)
                self.kb = bw.backward_coeffs(self.kf, T)
                progress.append(self.progress_reaction(x, self.kf[i], self.v1[i], kb=self.kb[i], v2=self.v2[i]))
            elif self.reversible[i] == 'no':
                progress.append(self.progress_reaction(x, self.kf[i], self.v1[i]))
            else:
                raise ValueError("Invalid reversibility type. Please check your XML file.")

        return progress

    def reaction_rates(self, x, T):
        """Returns the reaction rate of a system of reactions for each specie.

        INPUTS
        =======
        x: float, list of n, where n is the number of species
           concentrations of each species
        T: float, required
           environment temperature, used to calculate reaction rate coefficients

        RETURNS
        ========
        reaction rate: list of rate of consumption or formation of specie

        EXAMPLES
        ========
        >>> test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests/')
        >>> fname = os.path.join(test_data_dir, 'rxns.xml')
        >>> c = chemkin(fname)
        >>> c.reaction_rates([2., 1., .5, 1., 1., 1.], 1500)
        [-227364086.53073898, 227364586.53073898, 231985198.37073097, -2311055.9199959813, 500.0, -229675142.45073497]
        """
        try:
            self.parseNASA(T)
        except:
            raise ValueError("NASA parsing failed. Please check your database.")

        self.k_system(T)

        if np.array(self.v1).shape != np.array(self.v2).shape:
            raise ValueError("Dimensions of coefficients of reactants and products do not match.")
        for lst in self.v2:
            if any(isinstance(d, complex) for d in lst) == True:
                raise ValueError('Complex value in product coefficient detected!')

        progress = self.progress_system(x, T)
        reaction_rates = []

        for i in range(len(x)):
            reaction_rates.append(0)
            for j in range(len(progress)):
                reaction_rates[i] = reaction_rates[i] + ((self.v2[j][i]-self.v1[j][i])*progress[j])
        return reaction_rates

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        class_name = type(self).__name__
        return class_name + '()'

    #1. Nuclear reactions:
    #def detect nuclear_reaction_type():

    #2. Visualise half lives
    #def visualise_decay():
