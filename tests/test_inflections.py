
from nose.tools import eq_, assert_not_equal

import inflect


def is_eq(p, a, b):
    return (p.compare(a, b) or
            p.plnounequal(a, b) or
            p.plverbequal(a, b) or
            p.pladjequal(a, b))


def test_many():
    p = inflect.engine()

    data = get_data()

    for line in data:
        if 'TODO:' in line:
            continue
        try:
            singular, rest = line.split('->', 1)
        except ValueError:
            continue
        singular = singular.strip()
        rest = rest.strip()
        try:
            plural, comment = rest.split('#', 1)
        except ValueError:
            plural = rest.strip()
            comment = ''
        try:
            mod_plural, class_plural = plural.split("|", 1)
            mod_plural = mod_plural.strip()
            class_plural = class_plural.strip()
        except ValueError:
            mod_plural = class_plural = plural.strip()
        if 'verb' in comment.lower():
            is_nv = '_V'
        elif 'noun' in comment.lower():
            is_nv = '_N'
        else:
            is_nv = ''

        p.classical(all=0, names=0)
        mod_PL_V = p.plural_verb(singular)
        mod_PL_N = p.plural_noun(singular)
        mod_PL = p.plural(singular)
        if is_nv == '_V':
            mod_PL_val = mod_PL_V
        elif is_nv == '_N':
            mod_PL_val = mod_PL_N
        else:
            mod_PL_val = mod_PL

        p.classical(all=1)
        class_PL_V = p.plural_verb(singular)
        class_PL_N = p.plural_noun(singular)
        class_PL = p.plural(singular)
        if is_nv == '_V':
            class_PL_val = class_PL_V
        elif is_nv == '_N':
            class_PL_val = class_PL_N
        else:
            class_PL_val = class_PL

        yield check_all, p, is_nv, singular, mod_PL_val, class_PL_val, mod_plural, class_plural


def check_all(p, is_nv, singular, mod_PL_val, class_PL_val, mod_plural, class_plural):
    eq_(mod_plural, mod_PL_val)
    eq_(class_plural, class_PL_val)
    eq_(is_eq(p, singular, mod_plural) in ('s:p', 'p:s', 'eq'), True,
        msg='is_eq(%s,%s) == %s != %s' % (
            singular,
            mod_plural,
            is_eq(p, singular, mod_plural),
            's:p, p:s or eq'))
    eq_(is_eq(p, mod_plural, singular) in ('p:s', 's:p', 'eq'), True,
        msg='is_eq(%s,%s) == %s != %s' % (
            mod_plural,
            singular,
            is_eq(p, mod_plural, singular),
            's:p, p:s or eq'))
    eq_(is_eq(p, singular, class_plural) in ('s:p', 'p:s', 'eq'), True)
    eq_(is_eq(p, class_plural, singular) in ('p:s', 's:p', 'eq'), True)
    assert_not_equal(singular, '')
    eq_(mod_PL_val, mod_PL_val if class_PL_val else '%s|%s' (mod_PL_val, class_PL_val))

    if is_nv != '_V':
        eq_(p.singular_noun(mod_plural, 1), singular,
            msg="p.singular_noun(%s) == %s != %s" % (
                mod_plural, p.singular_noun(mod_plural, 1), singular))

        eq_(p.singular_noun(class_plural, 1), singular,
            msg="p.singular_noun(%s) == %s != %s" % (
                class_plural, p.singular_noun(class_plural, 1), singular))

    '''
    don't see any test data for this ???
    elsif (/^\s+(an?)\s+(.*?)\s*$/)
    {
        $article = $1
        $word    = $2
        $Aword   = A($word)

        ok ("$article $word" eq $Aword, "$article $word")
    }
    '''


def test_def():
    p = inflect.engine()

    p.defnoun("kin", "kine")
    p.defnoun('(.*)x', '$1xen')

    p.defverb('foobar',  'feebar',
              'foobar',  'feebar',
              'foobars', 'feebar')

    p.defadj('red', 'red|gules')

    eq_(p.no("kin", 0), "no kine", msg="kin -> kine (user defined)...")
    eq_(p.no("kin", 1), "1 kin")
    eq_(p.no("kin", 2), "2 kine")

    eq_(p.no("regex", 0), "no regexen", msg="regex -> regexen (user defined)")

    eq_(p.plural("foobar", 2), "feebar", msg="foobar -> feebar (user defined)...")
    eq_(p.plural("foobars", 2), "feebar")

    eq_(p.plural("red", 0), "red", msg="red -> red...")
    eq_(p.plural("red", 1), "red")
    eq_(p.plural("red", 2), "red")
    p.classical(all=True)
    eq_(p.plural("red", 0), "red", msg="red -> gules...")
    eq_(p.plural("red", 1), "red")
    eq_(p.plural("red", 2), "gules")


def test_ordinal():
    p = inflect.engine()
    eq_(p.ordinal(0), "0th", msg="0 -> 0th...")
    eq_(p.ordinal(1), "1st")
    eq_(p.ordinal(2), "2nd")
    eq_(p.ordinal(3), "3rd")
    eq_(p.ordinal(4), "4th")
    eq_(p.ordinal(5), "5th")
    eq_(p.ordinal(6), "6th")
    eq_(p.ordinal(7), "7th")
    eq_(p.ordinal(8), "8th")
    eq_(p.ordinal(9), "9th")
    eq_(p.ordinal(10), "10th")
    eq_(p.ordinal(11), "11th")
    eq_(p.ordinal(12), "12th")
    eq_(p.ordinal(13), "13th")
    eq_(p.ordinal(14), "14th")
    eq_(p.ordinal(15), "15th")
    eq_(p.ordinal(16), "16th")
    eq_(p.ordinal(17), "17th")
    eq_(p.ordinal(18), "18th")
    eq_(p.ordinal(19), "19th")
    eq_(p.ordinal(20), "20th")
    eq_(p.ordinal(21), "21st")
    eq_(p.ordinal(22), "22nd")
    eq_(p.ordinal(23), "23rd")
    eq_(p.ordinal(24), "24th")
    eq_(p.ordinal(100), "100th")
    eq_(p.ordinal(101), "101st")
    eq_(p.ordinal(102), "102nd")
    eq_(p.ordinal(103), "103rd")
    eq_(p.ordinal(104), "104th")

    eq_(p.ordinal('zero'), "zeroth", msg="zero -> zeroth...")
    eq_(p.ordinal('one'), "first")
    eq_(p.ordinal('two'), "second")
    eq_(p.ordinal('three'), "third")
    eq_(p.ordinal('four'), "fourth")
    eq_(p.ordinal('five'), "fifth")
    eq_(p.ordinal('six'), "sixth")
    eq_(p.ordinal('seven'), "seventh")
    eq_(p.ordinal('eight'), "eighth")
    eq_(p.ordinal('nine'), "ninth")
    eq_(p.ordinal('ten'), "tenth")
    eq_(p.ordinal('eleven'), "eleventh")
    eq_(p.ordinal('twelve'), "twelfth")
    eq_(p.ordinal('thirteen'), "thirteenth")
    eq_(p.ordinal('fourteen'), "fourteenth")
    eq_(p.ordinal('fifteen'), "fifteenth")
    eq_(p.ordinal('sixteen'), "sixteenth")
    eq_(p.ordinal('seventeen'), "seventeenth")
    eq_(p.ordinal('eighteen'), "eighteenth")
    eq_(p.ordinal('nineteen'), "nineteenth")
    eq_(p.ordinal('twenty'), "twentieth")
    eq_(p.ordinal('twenty-one'), "twenty-first")
    eq_(p.ordinal('twenty-two'), "twenty-second")
    eq_(p.ordinal('twenty-three'), "twenty-third")
    eq_(p.ordinal('twenty-four'), "twenty-fourth")
    eq_(p.ordinal('one hundred'), "one hundredth")
    eq_(p.ordinal('one hundred and one'), "one hundred and first")
    eq_(p.ordinal('one hundred and two'), "one hundred and second")
    eq_(p.ordinal('one hundred and three'), "one hundred and third")
    eq_(p.ordinal('one hundred and four'), "one hundred and fourth")


def test_prespart():
    p = inflect.engine()
    eq_(p.present_participle("sees"), "seeing", msg="sees -> seeing...")
    eq_(p.present_participle("eats"), "eating")
    eq_(p.present_participle("bats"), "batting")
    eq_(p.present_participle("hates"), "hating")
    eq_(p.present_participle("spies"), "spying")
    eq_(p.present_participle("skis"), "skiing")


def get_data():
    return '''
                    a  ->  as                             # NOUN FORM
      TODO:sing              a  ->  some                           # INDEFINITE ARTICLE
      TODO:  A.C.R.O.N.Y.M.  ->  A.C.R.O.N.Y.M.s
             abscissa  ->  abscissas|abscissae
             Achinese  ->  Achinese
            acropolis  ->  acropolises
                adieu  ->  adieus|adieux
     adjutant general  ->  adjutant generals
                aegis  ->  aegises
             afflatus  ->  afflatuses
               afreet  ->  afreets|afreeti
                afrit  ->  afrits|afriti
              agendum  ->  agenda
         aide-de-camp  ->  aides-de-camp
             Alabaman  ->  Alabamans
               albino  ->  albinos
                album  ->  albums
             Alfurese  ->  Alfurese
                 alga  ->  algae
                alias  ->  aliases
                 alto  ->  altos|alti
               alumna  ->  alumnae
              alumnus  ->  alumni
             alveolus  ->  alveoli
   TODO:siverb                am  ->  are
   TODO:siverb          am going  ->  are going
  ambassador-at-large  ->  ambassadors-at-large
            Amboinese  ->  Amboinese
          Americanese  ->  Americanese
               amoeba  ->  amoebas|amoebae
              Amoyese  ->  Amoyese
   TODO:siadj                an  ->  some                           # INDEFINITE ARTICLE
             analysis  ->  analyses
             anathema  ->  anathemas|anathemata
           Andamanese  ->  Andamanese
             Angolese  ->  Angolese
             Annamese  ->  Annamese
              antenna  ->  antennas|antennae
                 anus  ->  anuses
                 apex  ->  apexes|apices
   TODO:siadj            apex's  ->  apexes'|apices'                # POSSESSIVE FORM
             aphelion  ->  aphelia
            apparatus  ->  apparatuses|apparatus
             appendix  ->  appendixes|appendices
                apple  ->  apples
             aquarium  ->  aquariums|aquaria
            Aragonese  ->  Aragonese
            Arakanese  ->  Arakanese
          archipelago  ->  archipelagos
   TODO:siverb               are  ->  are
   TODO:siverb          are made  ->  are made
            armadillo  ->  armadillos
             arpeggio  ->  arpeggios
            arthritis  ->  arthritises|arthritides
             asbestos  ->  asbestoses
            asparagus  ->  asparaguses
                  ass  ->  asses
             Assamese  ->  Assamese
               asylum  ->  asylums
            asyndeton  ->  asyndeta
                at it  ->  at them                        # ACCUSATIVE
               ataman  ->  atamans
   TODO:siverb               ate  ->  ate
                atlas  ->  atlases|atlantes
                atman  ->  atmas
  TODO:singular_noun   attorney general  ->  attorneys general
   attorney of record  ->  attorneys of record
               aurora  ->  auroras|aurorae
                 auto  ->  autos
           auto-da-fe  ->  autos-da-fe
             aviatrix  ->  aviatrixes|aviatrices
    TODO:siadj       aviatrix's  ->  aviatrixes'|aviatrices'
           Avignonese  ->  Avignonese
                  axe  ->  axes
    TODO:singular_noun 2 anwers!            axis  ->  axes
                axman  ->  axmen
        Azerbaijanese  ->  Azerbaijanese
             bacillus  ->  bacilli
            bacterium  ->  bacteria
              Bahaman  ->  Bahamans
             Balinese  ->  Balinese
               bamboo  ->  bamboos
                banjo  ->  banjoes
                 bass  ->  basses                         # INSTRUMENT, NOT FISH
                basso  ->  bassos|bassi
               bathos  ->  bathoses
                 beau  ->  beaus|beaux
                 beef  ->  beefs|beeves
           beneath it  ->  beneath them                   # ACCUSATIVE
            Bengalese  ->  Bengalese
                 bent  ->  bent                           # VERB FORM
                 bent  ->  bents                          # NOUN FORM
              Bernese  ->  Bernese
            Bhutanese  ->  Bhutanese
                 bias  ->  biases
               biceps  ->  biceps
                bison  ->  bisons|bison
               blouse  ->  blouses
            Bolognese  ->  Bolognese
                bonus  ->  bonuses
             Borghese  ->  Borghese
                 boss  ->  bosses
            Bostonese  ->  Bostonese
                  box  ->  boxes
                  boy  ->  boys
                bravo  ->  bravoes
                bream  ->  bream
             breeches  ->  breeches
          bride-to-be  ->  brides-to-be
    Brigadier General  ->  Brigadier Generals
             britches  ->  britches
           bronchitis  ->  bronchitises|bronchitides
             bronchus  ->  bronchi
              brother  ->  brothers|brethren
   TODO:         brother's  ->  brothers'|brethren's
              buffalo  ->  buffaloes|buffalo
             Buginese  ->  Buginese
                 buoy  ->  buoys
               bureau  ->  bureaus|bureaux
               Burman  ->  Burmans
              Burmese  ->  Burmese
             bursitis  ->  bursitises|bursitides
                  bus  ->  buses
                 buzz  ->  buzzes
               buzzes  ->  buzz                           # VERB FORM
                by it  ->  by them                        # ACCUSATIVE
               caddis  ->  caddises
               caiman  ->  caimans
                 cake  ->  cakes
            Calabrese  ->  Calabrese
                 calf  ->  calves
               callus  ->  calluses
          Camaldolese  ->  Camaldolese
                cameo  ->  cameos
               campus  ->  campuses
                  can  ->  cans                           # NOUN FORM
                  can  ->  can                            # VERB FORM (all pers.)
                can't  ->  can't                          # VERB FORM
          candelabrum  ->  candelabra
             cannabis  ->  cannabises
      TODO:siverb         canoes  ->  canoe
                canto  ->  cantos
            Cantonese  ->  Cantonese
               cantus  ->  cantus
               canvas  ->  canvases
              CAPITAL  ->  CAPITALS
            carcinoma  ->  carcinomas|carcinomata
                 care  ->  cares
                cargo  ->  cargoes
              caribou  ->  caribous|caribou
            Carlylese  ->  Carlylese
               carmen  ->  carmina
                 carp  ->  carp
            Cassinese  ->  Cassinese
                  cat  ->  cats
              catfish  ->  catfish
               cayman  ->  caymans
             Celanese  ->  Celanese
              ceriman  ->  cerimans
               cervid  ->  cervids
            Ceylonese  ->  Ceylonese
             chairman  ->  chairmen
              chamois  ->  chamois
                chaos  ->  chaoses
              chapeau  ->  chapeaus|chapeaux
             charisma  ->  charismas|charismata
    TODO:siverb           chases  ->  chase
              chassis  ->  chassis
              chateau  ->  chateaus|chateaux
               cherub  ->  cherubs|cherubim
           chickenpox  ->  chickenpox
                chief  ->  chiefs
                child  ->  children
              Chinese  ->  Chinese
               chorus  ->  choruses
            chrysalis  ->  chrysalises|chrysalides
               church  ->  churches
             cicatrix  ->  cicatrixes|cicatrices
               circus  ->  circuses
                class  ->  classes
              classes  ->  class                          # VERB FORM
             clippers  ->  clippers
             clitoris  ->  clitorises|clitorides
                  cod  ->  cod
                codex  ->  codices
               coitus  ->  coitus
             commando  ->  commandos
           compendium  ->  compendiums|compendia
                coney  ->  coneys
             Congoese  ->  Congoese
            Congolese  ->  Congolese
           conspectus  ->  conspectuses
            contralto  ->  contraltos|contralti
          contretemps  ->  contretemps
            conundrum  ->  conundrums
                corps  ->  corps
               corpus  ->  corpuses|corpora
               cortex  ->  cortexes|cortices
               cosmos  ->  cosmoses
     TODO:singular_noun   court martial  ->  courts martial
                  cow  ->  cows|kine
              cranium  ->  craniums|crania
            crescendo  ->  crescendos
            criterion  ->  criteria
           curriculum  ->  curriculums|curricula
                czech  ->  czechs
                 dais  ->  daises
           data point  ->  data points
                datum  ->  data
               debris  ->  debris
              decorum  ->  decorums
                 deer  ->  deer
           delphinium  ->  delphiniums
          desideratum  ->  desiderata
               desman  ->  desmans
             diabetes  ->  diabetes
               dictum  ->  dictums|dicta
    TODO:siverb              did  ->  did
    TODO:siverb         did need  ->  did need
            digitalis  ->  digitalises
                dingo  ->  dingoes
              diploma  ->  diplomas|diplomata
               discus  ->  discuses
                 dish  ->  dishes
                ditto  ->  dittos
                djinn  ->  djinn
     TODO:siverb            does  ->  do
     TODO:siverb         doesn't  ->  don't                          # VERB FORM
                  dog  ->  dogs
                dogma  ->  dogmas|dogmata
               dolman  ->  dolmans
           dominatrix  ->  dominatrixes|dominatrices
               domino  ->  dominoes
            Dongolese  ->  Dongolese
             dormouse  ->  dormice
                drama  ->  dramas|dramata
                 drum  ->  drums
                dwarf  ->  dwarves
               dynamo  ->  dynamos
                edema  ->  edemas|edemata
                eland  ->  elands|eland
                  elf  ->  elves
                  elk  ->  elks|elk
               embryo  ->  embryos
             emporium  ->  emporiums|emporia
         encephalitis  ->  encephalitises|encephalitides
             enconium  ->  enconiums|enconia
                enema  ->  enemas|enemata
               enigma  ->  enigmas|enigmata
            epidermis  ->  epidermises
           epididymis  ->  epididymises|epididymides
              erratum  ->  errata
                ethos  ->  ethoses
           eucalyptus  ->  eucalyptuses
               eunuch  ->  eunuchs
             extremum  ->  extrema
                 eyas  ->  eyases
             factotum  ->  factotums
               farman  ->  farmans
              Faroese  ->  Faroese
                fauna  ->  faunas|faunae
                  fax  ->  faxes
            Ferrarese  ->  Ferrarese
                ferry  ->  ferries
                fetus  ->  fetuses
               fiance  ->  fiances
              fiancee  ->  fiancees
               fiasco  ->  fiascos
                 fish  ->  fish
                 fizz  ->  fizzes
             flamingo  ->  flamingoes
         flittermouse  ->  flittermice
     TODO:siverb           floes  ->  floe
                flora  ->  floras|florae
             flounder  ->  flounder
                focus  ->  focuses|foci
               foetus  ->  foetuses
                folio  ->  folios
           Foochowese  ->  Foochowese
                 foot  ->  feet
     TODO:siadj          foot's  ->  feet's                         # POSSESSIVE FORM
              foramen  ->  foramens|foramina
     TODO:siverb       foreshoes  ->  foreshoe
              formula  ->  formulas|formulae
                forum  ->  forums
     TODO:siverb          fought  ->  fought
                  fox  ->  foxes
     TODO:singular_noun 2 different returns        from him  ->  from them
              from it  ->  from them                      # ACCUSATIVE
               fungus  ->  funguses|fungi
             Gabunese  ->  Gabunese
              gallows  ->  gallows
             ganglion  ->  ganglions|ganglia
                  gas  ->  gases
               gateau  ->  gateaus|gateaux
    TODO:siverb             gave  ->  gave
              general  ->  generals
        generalissimo  ->  generalissimos
             Genevese  ->  Genevese
                genie  ->  genies|genii
    TODO:singular_noun 2 diff return values!           genius  ->  geniuses|genii
              Genoese  ->  Genoese
                genus  ->  genera
               German  ->  Germans
               ghetto  ->  ghettos
           Gilbertese  ->  Gilbertese
              glottis  ->  glottises
              Goanese  ->  Goanese
                 goat  ->  goats
                goose  ->  geese
    TODO:singular_noun Governor General  ->  Governors General
                  goy  ->  goys|goyim
             graffiti  ->  graffiti
    TODO:singular_noun 2 diff ret values         graffito  ->  graffiti
              grizzly  ->  grizzlies
                guano  ->  guanos
            guardsman  ->  guardsmen
             Guianese  ->  Guianese
                gumma  ->  gummas|gummata
    TODO:siverb         gumshoes  ->  gumshoe
               gunman  ->  gunmen
            gymnasium  ->  gymnasiums|gymnasia
    TODO:siverb              had  ->  had
    TODO:siverb      had thought  ->  had thought
            Hainanese  ->  Hainanese
    TODO:siverb       hammertoes  ->  hammertoe
         handkerchief  ->  handkerchiefs
             Hararese  ->  Hararese
            Harlemese  ->  Harlemese
               harman  ->  harmans
            harmonium  ->  harmoniums
    TODO:siverb              has  ->  have
    TODO:siverb       has become  ->  have become
    TODO:siverb         has been  ->  have been
    TODO:siverb         has-been  ->  has-beens
               hasn't  ->  haven't                        # VERB FORM
             Havanese  ->  Havanese
    TODO:siverb             have  ->  have
    TODO:siverb    have conceded  ->  have conceded
    TODO:singular_noun 2 values               he  ->  they
         headquarters  ->  headquarters
            Heavenese  ->  Heavenese
                helix  ->  helices
            hepatitis  ->  hepatitises|hepatitides
    TODO:singular_noun 2 values              her  ->  them                           # PRONOUN
    TODO:singular_noun 2 values              her  ->  their
         # POSSESSIVE ADJ
                 hero  ->  heroes
               herpes  ->  herpes
    TODO:singular_noun 2 values             hers  ->  theirs
         # POSSESSIVE NOUN
    TODO:singular_noun 2 values          herself  ->  themselves
               hetman  ->  hetmans
               hiatus  ->  hiatuses|hiatus
            highlight  ->  highlights
              hijinks  ->  hijinks
    TODO:singular_noun 2 values              him  ->  them
    TODO:singular_noun 2 values          himself  ->  themselves
         hippopotamus  ->  hippopotamuses|hippopotami
           Hiroshiman  ->  Hiroshimans
    TODO:singular_noun 2 values              his  ->  their
         # POSSESSIVE ADJ
    TODO:singular_noun 2 values              his  ->  theirs
         # POSSESSIVE NOUN
    TODO:siverb             hoes  ->  hoe
           honorarium  ->  honorariums|honoraria
                 hoof  ->  hoofs|hooves
           Hoosierese  ->  Hoosierese
    TODO:siverb       horseshoes  ->  horseshoe
         Hottentotese  ->  Hottentotese
                house  ->  houses
            housewife  ->  housewives
               hubris  ->  hubrises
                human  ->  humans
             Hunanese  ->  Hunanese
                hydra  ->  hydras|hydrae
           hyperbaton  ->  hyperbata
            hyperbola  ->  hyperbolas|hyperbolae
                    I  ->  we
                 ibis  ->  ibises
            ignoramus  ->  ignoramuses
              impetus  ->  impetuses|impetus
              incubus  ->  incubuses|incubi
                index  ->  indexes|indices
          Indochinese  ->  Indochinese
              inferno  ->  infernos
              innings  ->  innings
   TODO:singular_noun Inspector General  ->  Inspectors General
          interregnum  ->  interregnums|interregna
                 iris  ->  irises|irides
       TODO:siverb            is  ->  are
       TODO:siverb      is eaten  ->  are eaten
                isn't  ->  aren't                         # VERB FORM
                   it  ->  they                           # NOMINATIVE
       TODO:siadj           its  ->  their                          # POSSESSIVE FORM
               itself  ->  themselves
           jackanapes  ->  jackanapes
             Japanese  ->  Japanese
             Javanese  ->  Javanese
                Jerry  ->  Jerrys
                jerry  ->  jerries
                 jinx  ->  jinxes
               jinxes  ->  jinx                           # VERB FORM
           Johnsonese  ->  Johnsonese
                Jones  ->  Joneses
                jumbo  ->  jumbos
             Kanarese  ->  Kanarese
           Kiplingese  ->  Kiplingese
                knife  ->  knives                         # NOUN FORM
                knife  ->  knife                          # VERB FORM (1st/2nd pers.)
               knifes  ->  knife                          # VERB FORM (3rd pers.)
             Kongoese  ->  Kongoese
            Kongolese  ->  Kongolese
               lacuna  ->  lacunas|lacunae
      lady in waiting  ->  ladies in waiting
            Lapponese  ->  Lapponese
               larynx  ->  larynxes|larynges
                latex  ->  latexes|latices
               lawman  ->  lawmen
               layman  ->  laymen
                 leaf  ->  leaves                         # NOUN FORM
                 leaf  ->  leaf                           # VERB FORM (1st/2nd pers.)
                leafs  ->  leaf                           # VERB FORM (3rd pers.)
             Lebanese  ->  Lebanese
                leman  ->  lemans
                lemma  ->  lemmas|lemmata
                 lens  ->  lenses
              Leonese  ->  Leonese
      lick of the cat  ->  licks of the cat
   Lieutenant General  ->  Lieutenant Generals
                 life  ->  lives
                Liman  ->  Limans
                lingo  ->  lingos
                 loaf  ->  loaves
                locus  ->  loci
            Londonese  ->  Londonese
           Lorrainese  ->  Lorrainese
             lothario  ->  lotharios
                louse  ->  lice
             Lucchese  ->  Lucchese
              lumbago  ->  lumbagos
                lumen  ->  lumens|lumina
               lummox  ->  lummoxes
              lustrum  ->  lustrums|lustra
               lyceum  ->  lyceums
             lymphoma  ->  lymphomas|lymphomata
                 lynx  ->  lynxes
              Lyonese  ->  Lyonese
   TODO:            M.I.A.  ->  M.I.A.s
             Macanese  ->  Macanese
          Macassarese  ->  Macassarese
             mackerel  ->  mackerel
                macro  ->  macros
     TODO:siverb            made  ->  made
               madman  ->  madmen
             Madurese  ->  Madurese
                magma  ->  magmas|magmata
              magneto  ->  magnetos
        Major General  ->  Major Generals
           Malabarese  ->  Malabarese
              Maltese  ->  Maltese
                  man  ->  men
             mandamus  ->  mandamuses
            manifesto  ->  manifestos
               mantis  ->  mantises
              marquis  ->  marquises
                 Mary  ->  Marys
              maximum  ->  maximums|maxima
              measles  ->  measles
               medico  ->  medicos
               medium  ->  mediums|media
   TODO:siadj          medium's  ->  mediums'|media's
               medusa  ->  medusas|medusae
           memorandum  ->  memorandums|memoranda
             meniscus  ->  menisci
               merman  ->  mermen
            Messinese  ->  Messinese
        metamorphosis  ->  metamorphoses
           metropolis  ->  metropolises
                 mews  ->  mews
               miasma  ->  miasmas|miasmata
             Milanese  ->  Milanese
               milieu  ->  milieus|milieux
           millennium  ->  millenniums|millennia
              minimum  ->  minimums|minima
                 minx  ->  minxes
                 miss  ->  miss                           # VERB FORM (1st/2nd pers.)
                 miss  ->  misses                         # NOUN FORM
               misses  ->  miss                           # VERB FORM (3rd pers.)
    TODO:siverb       mistletoes  ->  mistletoe
             mittamus  ->  mittamuses
             Modenese  ->  Modenese
             momentum  ->  momentums|momenta
                money  ->  monies
             mongoose  ->  mongooses
                moose  ->  moose
        mother-in-law  ->  mothers-in-law
                mouse  ->  mice
                mumps  ->  mumps
             Muranese  ->  Muranese
                murex  ->  murices
               museum  ->  museums
            mustachio  ->  mustachios
   TODO:siadj                my  ->  our                            # POSSESSIVE FORM
               myself  ->  ourselves
               mythos  ->  mythoi
            Nakayaman  ->  Nakayamans
           Nankingese  ->  Nankingese
           nasturtium  ->  nasturtiums
            Navarrese  ->  Navarrese
               nebula  ->  nebulas|nebulae
             Nepalese  ->  Nepalese
             neuritis  ->  neuritises|neuritides
             neurosis  ->  neuroses
                 news  ->  news
                nexus  ->  nexus
              Niasese  ->  Niasese
           Nicobarese  ->  Nicobarese
               nimbus  ->  nimbuses|nimbi
            Nipponese  ->  Nipponese
                   no  ->  noes
               Norman  ->  Normans
              nostrum  ->  nostrums
             noumenon  ->  noumena
                 nova  ->  novas|novae
            nucleolus  ->  nucleoluses|nucleoli
              nucleus  ->  nuclei
                numen  ->  numina
                  oaf  ->  oafs
    TODO:siverb            oboes  ->  oboe
              occiput  ->  occiputs|occipita
               octavo  ->  octavos
              octopus  ->  octopuses|octopodes
               oedema  ->  oedemas|oedemata
            Oklahoman  ->  Oklahomans
              omnibus  ->  omnibuses
                on it  ->  on them                        # ACCUSATIVE
                 onus  ->  onuses
                opera  ->  operas
              optimum  ->  optimums|optima
                 opus  ->  opuses|opera
              organon  ->  organa
              ottoman  ->  ottomans
          ought to be  ->  ought to be                    # VERB (UNLIKE bride to be)
     TODO:siverb       overshoes  ->  overshoe
     TODO:siverb        overtoes  ->  overtoe
                 ovum  ->  ova
                   ox  ->  oxen
     TODO:siadj            ox's  ->  oxen's                         # POSSESSIVE FORM
                oxman  ->  oxmen
             oxymoron  ->  oxymorons|oxymora
              Panaman  ->  Panamans
             parabola  ->  parabolas|parabolae
              Parmese  ->  Parmese
               pathos  ->  pathoses
              pegasus  ->  pegasuses
            Pekingese  ->  Pekingese
               pelvis  ->  pelvises
             pendulum  ->  pendulums
                penis  ->  penises|penes
             penumbra  ->  penumbras|penumbrae
           perihelion  ->  perihelia
               person  ->  people|persons
              persona  ->  personae
            petroleum  ->  petroleums
              phalanx  ->  phalanxes|phalanges
                  PhD  ->  PhDs
           phenomenon  ->  phenomena
             philtrum  ->  philtrums
                photo  ->  photos
               phylum  ->  phylums|phyla
                piano  ->  pianos|piani
          Piedmontese  ->  Piedmontese
                 pika  ->  pikas
   TODO:singular_noun ret mul value            pincer  ->  pincers
              pincers  ->  pincers
            Pistoiese  ->  Pistoiese
              plateau  ->  plateaus|plateaux
                 play  ->  plays
               plexus  ->  plexuses|plexus
               pliers  ->  pliers
                plies  ->  ply                            # VERB FORM
                polis  ->  polises
             Polonese  ->  Polonese
             pontifex  ->  pontifexes|pontifices
          portmanteau  ->  portmanteaus|portmanteaux
           Portuguese  ->  Portuguese
               possum  ->  possums
               potato  ->  potatoes
                  pox  ->  pox
               pragma  ->  pragmas|pragmata
              premium  ->  premiums
          prima donna  ->  prima donnas|prime donne
                  pro  ->  pros
          proceedings  ->  proceedings
         prolegomenon  ->  prolegomena
                proof  ->  proofs
     proof of concept  ->  proofs of concept
          prosecutrix  ->  prosecutrixes|prosecutrices
           prospectus  ->  prospectuses|prospectus
            protozoan  ->  protozoans
            protozoon  ->  protozoa
                 puma  ->  pumas
     TODO:siverb             put  ->  put
              quantum  ->  quantums|quanta
 TODO:singular_noun quartermaster general  ->  quartermasters general
               quarto  ->  quartos
                 quiz  ->  quizzes
              quizzes  ->  quiz                           # VERB FORM
               quorum  ->  quorums
               rabies  ->  rabies
               radius  ->  radiuses|radii
                radix  ->  radices
               ragman  ->  ragmen
                rebus  ->  rebuses
   TODO:siverb            rehoes  ->  rehoe
             reindeer  ->  reindeer
   TODO:siverb           reshoes  ->  reshoe
                rhino  ->  rhinos
           rhinoceros  ->  rhinoceroses|rhinoceros
   TODO:siverb              roes  ->  roe
                  Rom  ->  Roma
            Romagnese  ->  Romagnese
                Roman  ->  Romans
             Romanese  ->  Romanese
               Romany  ->  Romanies
                romeo  ->  romeos
                 roof  ->  roofs
              rostrum  ->  rostrums|rostra
               ruckus  ->  ruckuses
               salmon  ->  salmon
            Sangirese  ->  Sangirese
   TODO: siverb              sank  ->  sank
           Sarawakese  ->  Sarawakese
              sarcoma  ->  sarcomas|sarcomata
            sassafras  ->  sassafrases
                  saw  ->  saw                            # VERB FORM (1st/2nd pers.)
                  saw  ->  saws                           # NOUN FORM
                 saws  ->  saw                            # VERB FORM (3rd pers.)
                scarf  ->  scarves
               schema  ->  schemas|schemata
             scissors  ->  scissors
             Scotsman  ->  Scotsmen
             sea-bass  ->  sea-bass
               seaman  ->  seamen
                 self  ->  selves
               Selman  ->  Selmans
           Senegalese  ->  Senegalese
               seraph  ->  seraphs|seraphim
               series  ->  series
    TODO:siverb        shall eat  ->  shall eat
               shaman  ->  shamans
              Shavese  ->  Shavese
            Shawanese  ->  Shawanese
    TODO:singular_noun multivalue              she  ->  they
                sheaf  ->  sheaves
               shears  ->  shears
                sheep  ->  sheep
                shelf  ->  shelves
   TODO:siverb             shoes  ->  shoe
   TODO:siverb       should have  ->  should have
              Siamese  ->  Siamese
              siemens  ->  siemens
              Sienese  ->  Sienese
            Sikkimese  ->  Sikkimese
                silex  ->  silices
              simplex  ->  simplexes|simplices
           Singhalese  ->  Singhalese
            Sinhalese  ->  Sinhalese
                sinus  ->  sinuses|sinus
                 size  ->  sizes
                sizes  ->  size                           #VERB FORM
             smallpox  ->  smallpox
                Smith  ->  Smiths
   TODO:siverb         snowshoes  ->  snowshoe
           Sogdianese  ->  Sogdianese
            soliloquy  ->  soliloquies
                 solo  ->  solos|soli
                 soma  ->  somas|somata
   TODO:singular_noun tough    son of a bitch  ->  sons of bitches
              Sonaman  ->  Sonamans
              soprano  ->  sopranos|soprani
   TODO:siverb            sought  ->  sought
   TODO:siverb       spattlehoes  ->  spattlehoe
              species  ->  species
             spectrum  ->  spectrums|spectra
             speculum  ->  speculums|specula
   TODO:siverb             spent  ->  spent
         spermatozoon  ->  spermatozoa
               sphinx  ->  sphinxes|sphinges
         spokesperson  ->  spokespeople|spokespersons
              stadium  ->  stadiums|stadia
               stamen  ->  stamens|stamina
               status  ->  statuses|status
               stereo  ->  stereos
               stigma  ->  stigmas|stigmata
             stimulus  ->  stimuli
                stoma  ->  stomas|stomata
              stomach  ->  stomachs
               storey  ->  storeys
                story  ->  stories
              stratum  ->  strata
               strife  ->  strifes
                stylo  ->  stylos
               stylus  ->  styluses|styli
             succubus  ->  succubuses|succubi
             Sudanese  ->  Sudanese
               suffix  ->  suffixes
            Sundanese  ->  Sundanese
             superior  ->  superiors
  TODO:singular_noun    Surgeon-General  ->  Surgeons-General
              surplus  ->  surpluses
            Swahilese  ->  Swahilese
                swine  ->  swines|swine
      TODO:singular_noun multiple return        syringe  ->  syringes
               syrinx  ->  syrinxes|syringes
              tableau  ->  tableaus|tableaux
              Tacoman  ->  Tacomans
              talouse  ->  talouses
               tattoo  ->  tattoos
               taxman  ->  taxmen
                tempo  ->  tempos|tempi
           Tenggerese  ->  Tenggerese
            testatrix  ->  testatrixes|testatrices
               testes  ->  testes
      TODO:singular_noun multiple return         testis  ->  testes
      TODO:siadj           that  ->  those
      TODO:siadj          their  ->  their
           # POSSESSIVE FORM (GENDER-INCLUSIVE)
      TODO:singular_noun multiple return       themself  ->  themselves
           # ugly but gaining currency
      TODO:singular_noun multiple return           they  ->  they
           # for indeterminate gender
                thief  ->  thiefs|thieves
      TODO:siadj           this  ->  these
              thought  ->  thoughts                       # NOUN FORM
              thought  ->  thought                        # VERB FORM
      TODO:siverb         throes  ->  throe
      TODO:siverb   ticktacktoes  ->  ticktacktoe
                Times  ->  Timeses
             Timorese  ->  Timorese
      TODO:siverb        tiptoes  ->  tiptoe
             Tirolese  ->  Tirolese
             titmouse  ->  titmice
      TODO:singular_noun multivalue         to her  ->  to them
      TODO:singular_noun multivalue     to herself  ->  to themselves
      TODO:singular_noun multivalue         to him  ->  to them
      TODO:singular_noun multivalue     to himself  ->  to themselves
                to it  ->  to them
                to it  ->  to them                        # ACCUSATIVE
            to itself  ->  to themselves
                to me  ->  to us
            to myself  ->  to ourselves
      TODO:singular_noun multivalue        to them  ->  to them
           # for indeterminate gender
      TODO:singular_noun multivalue    to themself  ->  to themselves
            # ugly but gaining currency
               to you  ->  to you
          to yourself  ->  to yourselves
            Tocharese  ->  Tocharese
      TODO:siverb           toes  ->  toe
               tomato  ->  tomatoes
            Tonkinese  ->  Tonkinese
          tonsillitis  ->  tonsillitises|tonsillitides
                tooth  ->  teeth
             Torinese  ->  Torinese
                torus  ->  toruses|tori
            trapezium  ->  trapeziums|trapezia
               trauma  ->  traumas|traumata
              travois  ->  travois
              trellis  ->  trellises
     TODO:siverb           tries  ->  try
               trilby  ->  trilbys
             trousers  ->  trousers
            trousseau  ->  trousseaus|trousseaux
                trout  ->  trout
      TODO:siverb            try  ->  tries
                 tuna  ->  tuna
                 turf  ->  turfs|turves
             Tyrolese  ->  Tyrolese
            ultimatum  ->  ultimatums|ultimata
            umbilicus  ->  umbilicuses|umbilici
                umbra  ->  umbras|umbrae
      TODO:siverb     undershoes  ->  undershoe
      TODO:siverb        unshoes  ->  unshoe
               uterus  ->  uteruses|uteri
               vacuum  ->  vacuums|vacua
               vellum  ->  vellums
                velum  ->  velums|vela
           Vermontese  ->  Vermontese
             Veronese  ->  Veronese
             vertebra  ->  vertebrae
               vertex  ->  vertexes|vertices
             Viennese  ->  Viennese
           Vietnamese  ->  Vietnamese
             virtuoso  ->  virtuosos|virtuosi
                virus  ->  viruses
                vixen  ->  vixens
               vortex  ->  vortexes|vortices
               walrus  ->  walruses
   TODO:siverb               was  ->  were
   TODO:siverb    was faced with  ->  were faced with
   TODO:siverb        was hoping  ->  were hoping
           Wenchowese  ->  Wenchowese
   TODO:siverb              were  ->  were
   TODO:siverb        were found  ->  were found
                wharf  ->  wharves
              whiting  ->  whiting
           Whitmanese  ->  Whitmanese
                 whiz  ->  whizzes
   TODO:singular_noun multivalue             whizz  ->  whizzes
               widget  ->  widgets
                 wife  ->  wives
           wildebeest  ->  wildebeests|wildebeest
                 will  ->  will                           # VERB FORM
                 will  ->  wills                          # NOUN FORM
             will eat  ->  will eat                       # VERB FORM
                wills  ->  will                           # VERB FORM
                 wish  ->  wishes
   TODO:singular_noun multivalue          with him  ->  with them
              with it  ->  with them                      # ACCUSATIVE
   TODO:siverb              woes  ->  woe
                 wolf  ->  wolves
                woman  ->  women
   woman of substance  ->  women of substance
    TODO:siadj          woman's  ->  women's                        # POSSESSIVE FORM
                won't  ->  won't                          # VERB FORM
            woodlouse  ->  woodlice
              Yakiman  ->  Yakimans
             Yengeese  ->  Yengeese
               yeoman  ->  yeomen
             yeowoman  ->  yeowomen
                  yes  ->  yeses
            Yokohaman  ->  Yokohamans
                  you  ->  you
   TODO:siadj              your  ->  your                           # POSSESSIVE FORM
             yourself  ->  yourselves
                Yuman  ->  Yumans
            Yunnanese  ->  Yunnanese
                 zero  ->  zeros
                 zoon  ->  zoa
'''.split('\n')
