'''
# Before `make install' is performed this script should be runnable with
# `make test'. After `make install' it should work as `perl test.pl'

######################### We start with some black magic to print on failure.

# Change 1..1 below to 1..last_test_to_print .
# (It may become useful if the test is moved to ./t subdirectory.)

END {print "not ok 1\n" unless $loaded;}
use Lingua::EN::Inflect qw( :ALL );
$loaded = 1;
print "ok 1\n";

my $count = 2;
sub ok($;$$)
{
    my $ok = $_[0];
    print "not " unless $ok;
    print "ok $count";
    print "\t# $_[1]" if $_[1];
    print " -> $_[2]" if $_[2];
    print "\n";
    $count++;
    return $ok;
}

######################### End of black magic.
'''
import unittest

import inflect

class test(unittest.TestCase):
    def is_eq(self, p, a, b):
        return (p.plequal(a, b) or
        p.plnounequal(a, b) or
        p.plverbequal(a, b) or
        p.pladjequal(a, b) )

    def test_many(self):

        p = inflect.engine()
        
        data = self.get_data()

        
        for line in data:
            if 'TODO:' in line:
                continue
            try:
                singular, rest = line.split('->',1)
            except ValueError:
                continue
            singular = singular.strip()
            rest = rest.strip()
            try:
                plural, comment = rest.split('#',1)
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
            mod_PL_V     = p.plverb(singular)
            mod_PL_N     = p.plnoun(singular)
            mod_PL       = p.pl(singular)
            if is_nv == '_V':
                mod_PL_val = mod_PL_V
            elif is_nv == '_N':
                mod_PL_val = mod_PL_N
            else:
                mod_PL_val = mod_PL


            p.classical(all=1)
            class_PL_V     = p.plverb(singular)
            class_PL_N     = p.plnoun(singular)
            class_PL       = p.pl(singular)
            if is_nv == '_V':
                class_PL_val = class_PL_V
            elif is_nv == '_N':
                class_PL_val = class_PL_N
            else:
                class_PL_val = class_PL


            self.assertEqual(mod_plural, mod_PL_val)
            self.assertEqual(class_plural, class_PL_val)
            self.assertEqual(self.is_eq(p, singular, mod_plural) in ('s:p', 'p:s', 'eq'), True, msg='is_eq(%s,%s) == %s != %s' % (singular, mod_plural,self.is_eq(p, singular, mod_plural), 's:p, p:s or eq'))
            self.assertEqual(self.is_eq(p, mod_plural, singular) in ('p:s', 's:p', 'eq'), True, msg='is_eq(%s,%s) == %s != %s' % (mod_plural, singular, self.is_eq(p, mod_plural, singular), 's:p, p:s or eq'))
            self.assertEqual(self.is_eq(p, singular, class_plural) in ('s:p', 'p:s', 'eq'), True)
            self.assertEqual(self.is_eq(p, class_plural, singular) in ('p:s', 's:p', 'eq'), True)
            self.assertNotEqual(singular, '')
            self.assertEqual(mod_PL_val, mod_PL_val if class_PL_val else '%s|%s' (mod_PL_val, class_PL_val))
        

            '''
            don't see any test data for this ???
            elsif (/^\s+(an?)\s+(.*?)\s*$/)
            {
                $article = $1;
                $word    = $2;
                $Aword   = A($word);
        
                ok ("$article $word" eq $Aword, "$article $word");
            }
            '''

    def test_def(self):
        p = inflect.engine()
        
        p.defnoun("kin", "kine")
        p.defnoun('(.*)x', '$1xen')

        p.defverb('foobar' , 'feebar',
                 'foobar' , 'feebar',
                 'foobars', 'feebar')
        
        p.defadj('red', 'red|gules')
        
        self.assertEqual( p.no("kin",0),  "no kine", msg="kin -> kine (user defined)..." );
        self.assertEqual( p.no("kin",1),  "1 kin" );
        self.assertEqual( p.no("kin",2),  "2 kine" );
        
        self.assertEqual( p.no("regex",0),  "no regexen", msg="regex -> regexen (user defined)" );

        self.assertEqual( p.pl("foobar",2),  "feebar", msg="foobar -> feebar (user defined)..." );
        self.assertEqual( p.pl("foobars",2),  "feebar" );

        self.assertEqual( p.pl("red",0),  "red", msg="red -> red..." );
        self.assertEqual( p.pl("red",1),  "red" );
        self.assertEqual( p.pl("red",2),  "red" );
        p.classical(1)
        self.assertEqual( p.pl("red",0),  "red" , msg="red -> gules...");
        self.assertEqual( p.pl("red",1),  "red" );
        self.assertEqual( p.pl("red",2),  "gules" );

    def test_ordinal(self):
        p = inflect.engine()
        self.assertEqual( p.ordinal(0),  "0th", msg="0 -> 0th..." );
        self.assertEqual( p.ordinal(1),  "1st" );
        self.assertEqual( p.ordinal(2),  "2nd" );
        self.assertEqual( p.ordinal(3),  "3rd" );
        self.assertEqual( p.ordinal(4),  "4th" );
        self.assertEqual( p.ordinal(5),  "5th" );
        self.assertEqual( p.ordinal(6),  "6th" );
        self.assertEqual( p.ordinal(7),  "7th" );
        self.assertEqual( p.ordinal(8),  "8th" );
        self.assertEqual( p.ordinal(9),  "9th" );
        self.assertEqual( p.ordinal(10),  "10th" );
        self.assertEqual( p.ordinal(11),  "11th" );
        self.assertEqual( p.ordinal(12),  "12th" );
        self.assertEqual( p.ordinal(13),  "13th" );
        self.assertEqual( p.ordinal(14),  "14th" );
        self.assertEqual( p.ordinal(15),  "15th" );
        self.assertEqual( p.ordinal(16),  "16th" );
        self.assertEqual( p.ordinal(17),  "17th" );
        self.assertEqual( p.ordinal(18),  "18th" );
        self.assertEqual( p.ordinal(19),  "19th" );
        self.assertEqual( p.ordinal(20),  "20th" );
        self.assertEqual( p.ordinal(21),  "21st" );
        self.assertEqual( p.ordinal(22),  "22nd" );
        self.assertEqual( p.ordinal(23),  "23rd" );
        self.assertEqual( p.ordinal(24),  "24th" );
        self.assertEqual( p.ordinal(100),  "100th" );
        self.assertEqual( p.ordinal(101),  "101st" );
        self.assertEqual( p.ordinal(102),  "102nd" );
        self.assertEqual( p.ordinal(103),  "103rd" );
        self.assertEqual( p.ordinal(104),  "104th" );

        self.assertEqual( p.ordinal('zero'),  "zeroth", msg="zero -> zeroth..." );
        self.assertEqual( p.ordinal('one'),  "first" );
        self.assertEqual( p.ordinal('two'),  "second" );
        self.assertEqual( p.ordinal('three'),  "third" );
        self.assertEqual( p.ordinal('four'),  "fourth" );
        self.assertEqual( p.ordinal('five'),  "fifth" );
        self.assertEqual( p.ordinal('six'),  "sixth" );
        self.assertEqual( p.ordinal('seven'),  "seventh" );
        self.assertEqual( p.ordinal('eight'),  "eighth" );
        self.assertEqual( p.ordinal('nine'),  "ninth" );
        self.assertEqual( p.ordinal('ten'),  "tenth" );
        self.assertEqual( p.ordinal('eleven'),  "eleventh" );
        self.assertEqual( p.ordinal('twelve'),  "twelfth" );
        self.assertEqual( p.ordinal('thirteen'),  "thirteenth" );
        self.assertEqual( p.ordinal('fourteen'),  "fourteenth" );
        self.assertEqual( p.ordinal('fifteen'),  "fifteenth" );
        self.assertEqual( p.ordinal('sixteen'),  "sixteenth" );
        self.assertEqual( p.ordinal('seventeen'),  "seventeenth" );
        self.assertEqual( p.ordinal('eighteen'),  "eighteenth" );
        self.assertEqual( p.ordinal('nineteen'),  "nineteenth" );
        self.assertEqual( p.ordinal('twenty'),  "twentieth" );
        self.assertEqual( p.ordinal('twenty-one'),  "twenty-first" );
        self.assertEqual( p.ordinal('twenty-two'),  "twenty-second" );
        self.assertEqual( p.ordinal('twenty-three'),  "twenty-third" );
        self.assertEqual( p.ordinal('twenty-four'),  "twenty-fourth" );
        self.assertEqual( p.ordinal('one hundred'),  "one hundredth" );
        self.assertEqual( p.ordinal('one hundred and one'),  "one hundred and first" );
        self.assertEqual( p.ordinal('one hundred and two'),  "one hundred and second" );
        self.assertEqual( p.ordinal('one hundred and three'),  "one hundred and third" );
        self.assertEqual( p.ordinal('one hundred and four'),  "one hundred and fourth" );

    def test_prespart(self):
        p = inflect.engine()
        self.assertEqual( p.prespart("sees"),  "seeing", msg="sees -> seeing..." );
        self.assertEqual( p.prespart("eats"),  "eating" );
        self.assertEqual( p.prespart("bats"),  "batting" );
        self.assertEqual( p.prespart("hates"),  "hating" );
        self.assertEqual( p.prespart("spies"),  "spying" );
        self.assertEqual( p.prespart("skis"),  "skiing" );

    def get_data(self):
        return '''
                    a  ->  as                             # NOUN FORM
                    a  ->  some                           # INDEFINITE ARTICLE
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
                   am  ->  are
             am going  ->  are going
  ambassador-at-large  ->  ambassadors-at-large
            Amboinese  ->  Amboinese
          Americanese  ->  Americanese
               amoeba  ->  amoebas|amoebae
              Amoyese  ->  Amoyese
                   an  ->  some                           # INDEFINITE ARTICLE
             analysis  ->  analyses
             anathema  ->  anathemas|anathemata
           Andamanese  ->  Andamanese
             Angolese  ->  Angolese
             Annamese  ->  Annamese
              antenna  ->  antennas|antennae
                 anus  ->  anuses
                 apex  ->  apexes|apices
               apex's  ->  apexes'|apices'                # POSSESSIVE FORM
             aphelion  ->  aphelia
            apparatus  ->  apparatuses|apparatus
             appendix  ->  appendixes|appendices
                apple  ->  apples
             aquarium  ->  aquariums|aquaria
            Aragonese  ->  Aragonese
            Arakanese  ->  Arakanese
          archipelago  ->  archipelagos
                  are  ->  are
             are made  ->  are made
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
                  ate  ->  ate
                atlas  ->  atlases|atlantes
                atman  ->  atmas
     attorney general  ->  attorneys general
   attorney of record  ->  attorneys of record
               aurora  ->  auroras|aurorae
                 auto  ->  autos
           auto-da-fe  ->  autos-da-fe
             aviatrix  ->  aviatrixes|aviatrices
           aviatrix's  ->  aviatrixes'|aviatrices'
           Avignonese  ->  Avignonese
                  axe  ->  axes
                 axis  ->  axes
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
               canoes  ->  canoe
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
               chases  ->  chase
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
        court martial  ->  courts martial
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
                  did  ->  did
             did need  ->  did need
            digitalis  ->  digitalises
                dingo  ->  dingoes
              diploma  ->  diplomas|diplomata
               discus  ->  discuses
                 dish  ->  dishes
                ditto  ->  dittos
                djinn  ->  djinn
                 does  ->  do
              doesn't  ->  don't                          # VERB FORM
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
                floes  ->  floe
                flora  ->  floras|florae
             flounder  ->  flounder
                focus  ->  focuses|foci
               foetus  ->  foetuses
                folio  ->  folios
           Foochowese  ->  Foochowese
                 foot  ->  feet
               foot's  ->  feet's                         # POSSESSIVE FORM
              foramen  ->  foramens|foramina
            foreshoes  ->  foreshoe
              formula  ->  formulas|formulae
                forum  ->  forums
               fought  ->  fought
                  fox  ->  foxes
             from him  ->  from them
              from it  ->  from them                      # ACCUSATIVE
               fungus  ->  funguses|fungi
             Gabunese  ->  Gabunese
              gallows  ->  gallows
             ganglion  ->  ganglions|ganglia
                  gas  ->  gases
               gateau  ->  gateaus|gateaux
                 gave  ->  gave
              general  ->  generals
        generalissimo  ->  generalissimos
             Genevese  ->  Genevese
                genie  ->  genies|genii
               genius  ->  geniuses|genii
              Genoese  ->  Genoese
                genus  ->  genera
               German  ->  Germans
               ghetto  ->  ghettos
           Gilbertese  ->  Gilbertese
              glottis  ->  glottises
              Goanese  ->  Goanese
                 goat  ->  goats
                goose  ->  geese
     Governor General  ->  Governors General
                  goy  ->  goys|goyim
             graffiti  ->  graffiti
             graffito  ->  graffiti
              grizzly  ->  grizzlies
                guano  ->  guanos
            guardsman  ->  guardsmen
             Guianese  ->  Guianese
                gumma  ->  gummas|gummata
             gumshoes  ->  gumshoe
               gunman  ->  gunmen
            gymnasium  ->  gymnasiums|gymnasia
                  had  ->  had
          had thought  ->  had thought
            Hainanese  ->  Hainanese
           hammertoes  ->  hammertoe
         handkerchief  ->  handkerchiefs
             Hararese  ->  Hararese
            Harlemese  ->  Harlemese
               harman  ->  harmans
            harmonium  ->  harmoniums
                  has  ->  have
           has become  ->  have become
             has been  ->  have been
             has-been  ->  has-beens
               hasn't  ->  haven't                        # VERB FORM
             Havanese  ->  Havanese
                 have  ->  have
        have conceded  ->  have conceded
                   he  ->  they
         headquarters  ->  headquarters
            Heavenese  ->  Heavenese
                helix  ->  helices
            hepatitis  ->  hepatitises|hepatitides
                  her  ->  them                           # PRONOUN
                  her  ->  their                          # POSSESSIVE ADJ
                 hero  ->  heroes
               herpes  ->  herpes
                 hers  ->  theirs                         # POSSESSIVE NOUN
              herself  ->  themselves
               hetman  ->  hetmans
               hiatus  ->  hiatuses|hiatus
            highlight  ->  highlights
              hijinks  ->  hijinks
                  him  ->  them
              himself  ->  themselves
         hippopotamus  ->  hippopotamuses|hippopotami
           Hiroshiman  ->  Hiroshimans
                  his  ->  their                          # POSSESSIVE ADJ
                  his  ->  theirs                         # POSSESSIVE NOUN
                 hoes  ->  hoe
           honorarium  ->  honorariums|honoraria
                 hoof  ->  hoofs|hooves
           Hoosierese  ->  Hoosierese
           horseshoes  ->  horseshoe
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
    Inspector General  ->  Inspectors General
          interregnum  ->  interregnums|interregna
                 iris  ->  irises|irides
                   is  ->  are
             is eaten  ->  are eaten
                isn't  ->  aren't                         # VERB FORM
                   it  ->  they                           # NOMINATIVE
                  its  ->  their                          # POSSESSIVE FORM
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
                 made  ->  made
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
             medium's  ->  mediums'|media's
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
           mistletoes  ->  mistletoe
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
                   my  ->  our                            # POSSESSIVE FORM
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
                oboes  ->  oboe
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
            overshoes  ->  overshoe
             overtoes  ->  overtoe
                 ovum  ->  ova
                   ox  ->  oxen
                 ox's  ->  oxen's                         # POSSESSIVE FORM
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
               pincer  ->  pincers
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
                  put  ->  put
              quantum  ->  quantums|quanta
quartermaster general  ->  quartermasters general
               quarto  ->  quartos
                 quiz  ->  quizzes
              quizzes  ->  quiz                           # VERB FORM
               quorum  ->  quorums
               rabies  ->  rabies
               radius  ->  radiuses|radii
                radix  ->  radices
               ragman  ->  ragmen
                rebus  ->  rebuses
               rehoes  ->  rehoe
             reindeer  ->  reindeer
              reshoes  ->  reshoe
                rhino  ->  rhinos
           rhinoceros  ->  rhinoceroses|rhinoceros
                 roes  ->  roe
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
                 sank  ->  sank
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
            shall eat  ->  shall eat
               shaman  ->  shamans
              Shavese  ->  Shavese
            Shawanese  ->  Shawanese
                  she  ->  they
                sheaf  ->  sheaves
               shears  ->  shears
                sheep  ->  sheep
                shelf  ->  shelves
                shoes  ->  shoe
          should have  ->  should have
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
            snowshoes  ->  snowshoe
           Sogdianese  ->  Sogdianese
            soliloquy  ->  soliloquies
                 solo  ->  solos|soli
                 soma  ->  somas|somata
       son of a bitch  ->  sons of bitches
              Sonaman  ->  Sonamans
              soprano  ->  sopranos|soprani
               sought  ->  sought
          spattlehoes  ->  spattlehoe
              species  ->  species
             spectrum  ->  spectrums|spectra
             speculum  ->  speculums|specula
                spent  ->  spent
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
      Surgeon-General  ->  Surgeons-General
              surplus  ->  surpluses
            Swahilese  ->  Swahilese
                swine  ->  swines|swine
              syringe  ->  syringes
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
               testis  ->  testes
                 that  ->  those
                their  ->  their                          # POSSESSIVE FORM (GENDER-INCLUSIVE)
             themself  ->  themselves                     # ugly but gaining currency
                 they  ->  they                           # for indeterminate gender
                thief  ->  thiefs|thieves
                 this  ->  these
              thought  ->  thoughts                       # NOUN FORM
              thought  ->  thought                        # VERB FORM
               throes  ->  throe
         ticktacktoes  ->  ticktacktoe
                Times  ->  Timeses
             Timorese  ->  Timorese
              tiptoes  ->  tiptoe
             Tirolese  ->  Tirolese
             titmouse  ->  titmice
               to her  ->  to them
           to herself  ->  to themselves
               to him  ->  to them
           to himself  ->  to themselves
                to it  ->  to them
                to it  ->  to them                        # ACCUSATIVE
            to itself  ->  to themselves
                to me  ->  to us
            to myself  ->  to ourselves
              to them  ->  to them                        # for indeterminate gender
          to themself  ->  to themselves                  # ugly but gaining currency
               to you  ->  to you
          to yourself  ->  to yourselves
            Tocharese  ->  Tocharese
                 toes  ->  toe
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
                tries  ->  try
               trilby  ->  trilbys
             trousers  ->  trousers
            trousseau  ->  trousseaus|trousseaux
                trout  ->  trout
                  try  ->  tries
                 tuna  ->  tuna
                 turf  ->  turfs|turves
             Tyrolese  ->  Tyrolese
            ultimatum  ->  ultimatums|ultimata
            umbilicus  ->  umbilicuses|umbilici
                umbra  ->  umbras|umbrae
           undershoes  ->  undershoe
              unshoes  ->  unshoe
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
                  was  ->  were
       was faced with  ->  were faced with
           was hoping  ->  were hoping
           Wenchowese  ->  Wenchowese
                 were  ->  were
           were found  ->  were found
                wharf  ->  wharves
              whiting  ->  whiting
           Whitmanese  ->  Whitmanese
                 whiz  ->  whizzes
                whizz  ->  whizzes
               widget  ->  widgets
                 wife  ->  wives
           wildebeest  ->  wildebeests|wildebeest
                 will  ->  will                           # VERB FORM
                 will  ->  wills                          # NOUN FORM
             will eat  ->  will eat                       # VERB FORM
                wills  ->  will                           # VERB FORM
                 wish  ->  wishes
             with him  ->  with them
              with it  ->  with them                      # ACCUSATIVE
                 woes  ->  woe
                 wolf  ->  wolves
                woman  ->  women
   woman of substance  ->  women of substance
              woman's  ->  women's                        # POSSESSIVE FORM
                won't  ->  won't                          # VERB FORM
            woodlouse  ->  woodlice
              Yakiman  ->  Yakimans
             Yengeese  ->  Yengeese
               yeoman  ->  yeomen
             yeowoman  ->  yeowomen
                  yes  ->  yeses
            Yokohaman  ->  Yokohamans
                  you  ->  you
                 your  ->  your                           # POSSESSIVE FORM
             yourself  ->  yourselves
                Yuman  ->  Yumans
            Yunnanese  ->  Yunnanese
                 zero  ->  zeros
                 zoon  ->  zoa
'''.split('\n')


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:
        pass

