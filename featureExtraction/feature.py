#import sys
#sys.path.append("..")
#from ..fileReading import Data
from .entity_dic import entity_dict
import gensim
import json
import os
import numpy as np
#import  .word_vector.word_vec_wrapper
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

realismap ={'actual':0, 'generic':1, 'other':2, 'non-event':4}

nermap = {'sentence':0, 'commodity':1, 'time':2, 'crime':3, 'LOC':4, 'vehicle':5, 'PER':6, 'money':7, 'GPE':8, 'weapon':9, 'ORG':10, 'title':11, 'FAC':12}

arg_specificity = {'nonspecific': 1, 'specificGroup': 3, 'specific': 0, 'specificIndeterminate': 5, 'specificIndividual': 4, 'UNK': 2}

arg_ere= {'ere::Beneficiary': 46, 'adjudicator': 38, 'person': 8, 'ere::Giver': 43, 'ere::Agent': 24, 'destination': 15, 'audience': 17, 'place': 18, 'ere::Destination': 42, 'ere::Audience': 45, 'ere::Adjudicator': 48, 'giver': 36, 'ere::Person': 23, 'defendant': 11, 'ere::Origin': 41, 'ere::Org': 25, 'recipient': 20, 'ere::Defendant': 33, 'ere::Position': 39, 'beneficiary': 40, 'attacker': 6, 'instrument': 7, 'ere::Money': 44, 'ere::Target': 2, 'entity': 9, 'artifact': 28, 'ere::Place': 3, 'target': 14, 'money': 32, 'ere::Victim': 27, 'crime': 19, 'position': 26, 'ere::Crime': 35, 'origin': 22, 'thing': 21, 'victim': 0, 'ere::Entity': 12, 'ere::Thing': 31, 'time': 13, 'prosecutor': 10, 'ere::Prosecutor': 37, 'agent': 1, 'ere::Instrument': 5, 'ere::Attacker': 4, 'ere::Sentence': 34, 'ere::Artifact': 16, 'ere::Recipient': 30, 'ere::Time': 29, 'ere::Plaintiff': 47}

event_ere_map = {'transportperson': 6, 'correspondence': 18, 'acquit': 33, 'transferownership': 8, 'extradite': 37, 'fine': 22, 'injure': 11, 'trialhearing': 4, 'attack': 1, 'beborn': 14, 'mergeorg': 21, 'transportartifact': 16, 'sue': 34, 'endorg': 30, 'transaction': 29, 'releaseparole': 32, 'arrestjail': 2, 'transfermoney': 17, 'divorce': 19, 'execute': 31, 'contact': 3, 'pardon': 26, 'meet': 13, 'startorg': 10, 'die': 0, 'appeal': 35, 'broadcast': 5, 'nominate': 20, 'convict': 24, 'endposition': 27, 'artifact': 7, 'declarebankruptcy': 36, 'demonstrate': 28, 'chargeindict': 25, 'startposition': 12, 'sentence': 23, 'marry': 15, 'elect': 9}

event_reo_map = {'reo::UNK': 0, 'reo::Give': 1, 'reo::Send': 2, 'reo::Physical_attack': 3, 'reo::Death': 4, 'reo::Get': 5, 'reo::Accompanied_directed_intrinsic_change_location': 6, 'reo::Kill': 7, 'reo::Instrument_Communication': 8, False: 9, 'reo::Intrinsic_change_location': 10, 'reo::Statement': 11, 'reo::Buy_sell': 12, 'reo::Accompanied_directed_caused_change_location': 13, 'reo::Execute': 14, 'reo::Exchange': 15, 'reo::Meet': 16, 'reo::Conversing': 17, 'reo::Lecture': 18, 'reo::Intrinsic_reach': 19, 'reo::Intrinsic_leave': 20, 'reo::Arrest': 21, 'reo::Steal': 22, 'reo::End_position_with_organization': 23, 'reo::Hiring': 24, 'reo::Appeal': 25, 'reo::Firing': 26, 'reo::Prosecute': 27, 'reo::Discharge': 28, 'reo::Verdict': 29, 'reo::Begin_leadership_position': 30, 'reo::End_leadership_position': 31, 'reo::Loan_borrow': 32, 'reo::Experience_Injury': 33, 'reo::Change_possession': 34, 'reo::Charge': 35, 'reo::Caused_leave-Remove': 36, 'reo::Protest_conflict': 37, 'reo::Put': 38, 'reo::Declarational': 39, 'reo::Birth': 40, 'reo::Pardon': 41, 'reo::Attitudinal': 42, 'reo::Extradite': 43, 'reo::Trajectory_focused_intrinsic_change_location': 44, 'reo::Divorce': 45, 'reo::Verbal_Communication': 46, 'reo::Response': 47, 'reo::Question': 48, 'reo::Marry': 49}

arg_reo_map = {'UNK': 0, 'reo::Donor': 1, 'reo::Recipient': 2, 'reo::Agent': 3, 'reo::Theme': 4, 'reo::Attacker': 5, 'reo::Target': 6, 'reo::Victim': 7, 'reo::AccompaniedTheme': 8, 'reo::Destination': 9, 'reo::Mover': 10, 'reo::place': 11, 'reo::Place': 12, 'reo::Time': 13, 'reo::time': 14, 'reo::CrimeOrCause': 15, 'reo::Meeting_Parties': 16, 'reo::Audience': 17, 'reo::ModeOfTransportation': 18, 'reo::Initial_Location': 19, 'reo::Suspect': 20, 'reo::Employee': 21, 'reo::Employer': 22, 'reo::Defendant': 23, 'reo::Position': 24, 'reo::CostOrCotheme': 25, 'reo::Adjudicator': 26, 'reo::Captive': 27, 'reo::GovernedEntity': 28, 'reo::Leader': 29, 'reo::Cause': 30, 'reo::Protester': 31, 'reo::Child': 32, 'reo::Weapon': 33, 'reo::Authority': 34, 'reo::Instrument': 35, 'reo::Couple': 36, 'reo::Prosecutor': 37, 'reo::Artifact': 38}
class Feature:
    def extract_feature(self, event,w2v):
        #---- event features-----#
        realis_1hot = [0]*len(realismap)
        realis_1hot[realismap[event['event']['modality']]]=1
        #if w2v != None:
            #word2vec_lemma = w2v.vector(event['event']['lemma'])#w2v[event['event']['lemma']]
        event_ere_presence = [0]*len(event_ere_map)
        ev_ere = event['event']['ere']
        event_ere_presence[event_ere_map[ev_ere]]+=1
        #----- argument features-----#
        args = event['arguments']
        no_of_args = len(args)
        arg_ere_presence = [0]*len(arg_ere)
        arg_specificity_presence = [0]*len(arg_specificity)
        arg_ner_presence = [0]*len(nermap)
        #arg_entity_presence = [0]*len(entity_dict)
        i=0
        arg_feature = list()
        while i<5:

            if i < len(args):
                a = args[i]
                ere = a['ere']
                sp = a['entity-specificity']
                ner = a['entity-ner']
                entity = a['entity']
                areo = a['reo']
                ## save zero to build zero vector for padding. Hence adding one to all
                arg_feature.append(arg_ere[ere]+1)
                arg_feature.append(arg_specificity[sp]+1)
                arg_feature.append(nermap[ner]+1)
                arg_feature.append(entity_dict[entity]+1)
                arg_feature.append(arg_reo_map[areo]+1)
            else:
                #zero vector padding
                arg_feature.append(0)
                arg_feature.append(0)
                arg_feature.append(0)
                arg_feature.append(0)
                arg_feature.append(0)
            i = i+1

        #--create the feature---#
        ev_feature = list()
        ev_feature.extend(realis_1hot)
        #if w2v != None:
            #ere_feature.extend(word2vec_lemma)
        ev_feature.extend(event_ere_presence)
        ev_feature.extend([no_of_args])
        feature = [arg_feature,ev_feature]
        #return np.array(feature)
        return [arg_feature,ev_feature]

if __name__ == '__main__':
    testfileName='/Users/abhipubali/Public/DropBox/AIDA_Paper/work/data/Inputs/010aaf594ae6ef20eb28e3ee26038375.rich_ere.xml.inputs.json'
    with open(testfileName) as json_data:
        data= json.load(json_data)
    ev= data[0]
    print(ev)
    feat = Feature()
    #w2v = KeyedVectors.load_word2vec_format('/Users/abhipubali/Public/DropBox/sem2_s18/chenhao_course/word_embeddings_benchmarks/scripts/word2vec_wikipedia/wiki_w2v_300.txt', binary=False)
    f= feat.extract_feature(ev, None)
    #print(f.shape)
    print(f)
