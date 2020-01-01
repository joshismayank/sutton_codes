#include <iostream>
#include <set>
#include <string>
#include <map>
#include <fstream>
#include <vector>
#include <time.h>

using namespace std;

struct action_data {
	int wins;
	int total_tries;
	float win_prob;
};

int total_wins, rndm;

map<int,vector<struct action_data *>> results;

void get_curr_player(string &curr_player) {
	if (curr_player == "dumb") {
		curr_player = "rl";
	} else {
		curr_player = "dumb";
	}
}

void get_curr_action(string &curr_player, int &curr_action) {
	if(curr_player == "rl") {
		curr_action = 1;
	} else {
		curr_action = -1;
	}
}

void perform_action(vector<int> &curr_board, int &curr_action, int &curr_action_pos) {
	curr_board[curr_action_pos] = curr_action;
}

void get_action_pos(int &curr_action, int &curr_action_pos, set<int> &curr_available_board, int &curr_itr, int &curr_state) {
	int pos, i, action_pos = -1;
	float max_prob = -1;
	if(curr_action == -1) {
		pos = rand() % (curr_available_board.size());
		set<int>::iterator it = curr_available_board.begin();
		std::advance(it, pos);
		curr_action_pos = *it;
	} else {
		if(results.find(curr_state) == results.end()) {
			rndm++;
			pos = rand() % (curr_available_board.size());
			set<int>::iterator it = curr_available_board.begin();
			std::advance(it, pos);
			curr_action_pos = *it;
		} else {
			vector<struct action_data*> the_data = results.find(curr_state)->second;
			for(i=0;i<9;i++) {
				if(curr_available_board.find(i) != curr_available_board.end() && the_data[i] != NULL) {
					if (the_data[i]->win_prob > max_prob) {
						action_pos = i;
					}
				}
			}
			if(action_pos != -1) {
				curr_action_pos = action_pos;
			} else {
				rndm++;
				pos = rand() % (curr_available_board.size());
				set<int>::iterator it = curr_available_board.begin();
				std::advance(it, pos);
				curr_action_pos = *it;
			}
		}
	}
	curr_available_board.erase(curr_action_pos);
}

void get_curr_status(string &curr_status, vector<int> &curr_board) {
	int i;
	for(i=0;i<9;i++) {
		if(curr_board[i] == 0) {
			curr_status = "undecided";
			return;
		}
	}
	if (curr_board[0]+curr_board[1]+curr_board[2]==3) {
		curr_status = "win";
	} else if (curr_board[3]+curr_board[4]+curr_board[5]==3) {
		curr_status = "win";
	} else if(curr_board[6]+curr_board[7]+curr_board[8]==3) {
		curr_status = "win";
	} else if(curr_board[0]+curr_board[3]+curr_board[6]==3) {
		curr_status = "win";
	} else if(curr_board[1]+curr_board[4]+curr_board[7]==3) {
		curr_status = "win";
	} else if(curr_board[2]+curr_board[5]+curr_board[8]==3) {
		curr_status = "win";
	} else if(curr_board[0]+curr_board[4]+curr_board[8]==3) {
		curr_status = "win";
	} else if(curr_board[2]+curr_board[4]+curr_board[6]==3) {
		curr_status = "win";
	} else if (curr_board[0]+curr_board[1]+curr_board[2]==-3) {
		curr_status = "lose";
	} else if (curr_board[3]+curr_board[4]+curr_board[5]==-3) {
		curr_status = "lose";
	} else if(curr_board[6]+curr_board[7]+curr_board[8]==-3) {
		curr_status = "lose";
	} else if(curr_board[0]+curr_board[3]+curr_board[6]==-3) {
		curr_status = "lose";
	} else if(curr_board[1]+curr_board[4]+curr_board[7]==-3) {
		curr_status = "lose";
	} else if(curr_board[2]+curr_board[5]+curr_board[8]==-3) {
		curr_status = "lose";
	} else if(curr_board[0]+curr_board[4]+curr_board[8]==-3) {
		curr_status = "lose";
	} else if(curr_board[2]+curr_board[4]+curr_board[6]==-3) {
		curr_status = "lose";
	} else {
		curr_status = "draw";
	}
}

void store_state_action(int &curr_state, vector<int> &curr_board, int &curr_action_pos, vector<int> &past_states, vector<int> &past_action_posns) {
	int i;
	for (i=0;i<9;i++) {
		curr_state += ((i+1)*(i+1)*curr_board[i]);
	}
	//cout<<"store: state - "<<curr_state<<" action_pos - "<<curr_action_pos<<"\t";
	past_states.push_back(curr_state);
	past_action_posns.push_back(curr_action_pos);
}

void update_result(string &curr_status, vector<int> &past_states, vector<int> &past_action_posns) {
	int len = past_states.size();
	int i, state, action_pos;
	int wins = 0;
	if (curr_status == "win") {
		wins++;
	}
	for(i=0;i<len;i++) {
		state = past_states[i];
		action_pos = past_action_posns[i];
		if(results.find(state) == results.end()) {
			struct action_data *new_action_data = (struct action_data*) malloc(sizeof(struct action_data));
			new_action_data->wins = wins;
			new_action_data->total_tries = 1;
			new_action_data->win_prob = wins;
			vector<struct action_data*> the_data = {NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL};
			the_data[action_pos] = new_action_data;
			results.insert(pair<int,vector<struct action_data *>>(state,the_data));
		} else {
			vector<struct action_data*> the_data = results.find(state)->second;
			struct action_data *continue_action_data = the_data[action_pos];
			if (continue_action_data == NULL) {
				continue_action_data = (struct action_data*) malloc(sizeof(struct action_data));
				continue_action_data->wins = wins;
				continue_action_data->total_tries = 1;
				continue_action_data->win_prob = wins;
				the_data[action_pos] = continue_action_data;
				results.find(state)->second = the_data;
			} else {
				continue_action_data->wins = continue_action_data->wins+wins;
				continue_action_data->total_tries = continue_action_data->total_tries+1;
				continue_action_data->win_prob = (((float)(continue_action_data->wins))/((float)(continue_action_data->total_tries)));
			}
		}
	}
}

void play_game(int curr_itr) {
	int temp_board[] = {0,1,2,3,4,5,6,7,8};
	set<int> curr_available_board(temp_board,temp_board+9);
	vector<int> curr_board = {0,0,0,0,0,0,0,0,0};
	vector<int> past_states;
	vector<int> past_action_posns;
	string curr_player;
	int curr_action;
	int curr_action_pos;
	int curr_state = 0;
	int i;
	string curr_status = "undecided";
	while (curr_status == "undecided") {
		get_curr_player(curr_player);
		get_curr_action(curr_player,curr_action);
		get_action_pos(curr_action,curr_action_pos,curr_available_board,curr_itr,curr_state);
		perform_action(curr_board,curr_action,curr_action_pos);
		get_curr_status(curr_status,curr_board);
		/*if(curr_player == "rl") {
			store_state_action(curr_state,curr_board,curr_action_pos,past_states,past_action_posns);
		}*/
	}
	if(curr_status == "win") {
		total_wins++;
	}
	//update_result(curr_status,past_states,past_action_posns);
}

void output_result_to_file() {
	ofstream the_file;
	int i, state, wins, total;
	int total_wins = 0;
	int total_total = 0;
	float prob;
	vector<struct action_data*> the_data_list;
	the_file.open("tic_tac_toe.csv");
	the_file<<"state,pos,wins,total_tries,win_prob,\n";
	for (auto const& it : results) {
		state = it.first;
		the_data_list = it.second;
		for(i=0;i<9;i++) {
			if(the_data_list[i] != NULL) {
				wins = the_data_list[i]->wins;
				total = the_data_list[i]->total_tries;
				prob = the_data_list[i]->win_prob;
				if(total>1) {
					cout<<"state: "<<state<<", wins: "<<wins<<", total: "<<total<<", prob: "<<prob<<"\n";
				}
				total_wins += wins;
				total_total += total;
				the_file<<state<<","<<i<<","<<wins<<","<<total<<","<<prob<<",\n";
			}
		}
	}
	cout<<"total wins: "<<total_wins<<", total: "<<total_total<<"\n";
	the_file.close();
}

void insert_result(int &state, int &action_pos, int &wins, int &total, float &prob) {
	if(results.find(state) == results.end()) {
		struct action_data *new_action_data = (struct action_data*) malloc(sizeof(struct action_data));
		new_action_data->wins = wins;
		new_action_data->total_tries = total;
		new_action_data->win_prob = prob;
		vector<struct action_data*> the_data = {NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL};
		the_data[action_pos] = new_action_data;
		results.insert(pair<int,vector<struct action_data *>>(state,the_data));
	} else {
		vector<struct action_data*> the_data = results.find(state)->second;
		struct action_data *continue_action_data = the_data[action_pos];
		if (continue_action_data == NULL) {
			continue_action_data = (struct action_data*) malloc(sizeof(struct action_data));
			continue_action_data->wins = wins;
			continue_action_data->total_tries = total;
			continue_action_data->win_prob = prob;
			the_data[action_pos] = continue_action_data;
			results.find(state)->second = the_data;
		} else {
			continue_action_data->wins = wins;
			continue_action_data->total_tries = total;
			continue_action_data->win_prob = prob;
		}
	}
}

void load_trained_data() {
	ifstream the_file;
	string line;
	string delim = ",";
	string state_str, action_pos_str, win_str, total_str, prob_str;
	int state_pos, action_pos_pos, win_pos, total_pos, prob_pos, state, wins, total, action_pos;
	float prob;
	the_file.open("tic_tac_toe.csv");
	string::size_type sz;
	while(getline(the_file, line)) {
		state_pos = line.find(delim,0);
		action_pos_pos = line.find(delim,state_pos+1);
		win_pos = line.find(delim,action_pos_pos+1);
		total_pos = line.find(delim,win_pos+1);
		prob_pos = line.find(delim,total_pos+1);
		state_str = line.substr(0,state_pos);
		action_pos_str = line.substr(state_pos+1,action_pos_pos-state_pos-1);
		win_str = line.substr(action_pos_pos+1,win_pos-action_pos_pos-1);
		total_str = line.substr(win_pos+1,total_pos-win_pos-1);
		prob_str = line.substr(total_pos+1,prob_pos-total_pos-1);
		try {
			state = stoi(state_str);
		} catch (...) {}
		try {
			action_pos = stoi(action_pos_str);
		} catch (...) {}
		try {
			wins = stoi(win_str);
		} catch (...) {}
		try {
			total = stoi(total_str);
		} catch (...) {}
		try {
			prob = stof(prob_str);
		} catch (...) {}
		insert_result(state,action_pos,wins,total,prob);
	}
}

int main() {
	int i, iterations;
	total_wins = 0;
	rndm = 0;
	load_trained_data();
	srand(time(NULL));
	cout<<"How many iterations?\n";
	cin>>iterations;
	for(i=0;i<iterations;i++) {
		play_game(i);
	}
	cout<<"total wins: "<<total_wins<<", random: "<<rndm<<"\n";
	//output_result_to_file();
	return 0;
}
