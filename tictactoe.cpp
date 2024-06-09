//Note: Must use MSVC windows. 
#include<iostream>
#include<utility>
#include<cstdio>
#include<cctype>
#include<string>
#include<cstdio>
#include<conio.h>
#include<vector>
#include<algorithm>
#include<random>
#include<Windows.h>
using namespace std;

struct Pos {
	int x, y;
};
enum gameState {
	O_won, X_won, Tie, gameOngoing
};
enum State {
	main_menu, play_game
};

class Input;
class Board {
	char board[3][3];
	char turn; //Keeps track of whether it's X or O's turn
	int turncnt{}; //Keeps track of the # of turns to end game in tie
	unique_ptr<Input> xInput, oInput; //The inputs given for X and O's
	//This is used as a unique pointer so more input methods could be added 
	//Currently there is only humaninput and random, an actual tictactoe AI could be added as another.
public:
	Board();
	void nextMove();
	void setInput(unique_ptr<Input>&&, unique_ptr<Input>&&);
	gameState getState();
	void display();
	const char* operator[](int a) {
		return board[a];
	}

};

class Input { //Abstract base class
public:
	virtual Pos getPos() = 0;
};
class humanInput : public Input {
public:
	Pos getPos();
};

class random : public Input {
	Board* b; //Needs tho board pointer to see what spots are available
public:
	void init_board(Board*);
	Pos getPos();
};
void random::init_board(Board* b) {
	this->b = b;
}
Pos random::getPos() { //Get a random position that is available on the board
	vector<Pos> available;
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if ((*b)[i][j] == ' ')available.push_back({ i,j });
		}
	}

	shuffle(available.begin(), available.end(),random_device());
	return available[0];
}

Pos humanInput::getPos() { //Gets human input
	cout << "Enter your move using 2 numbers. Row and column 1 indexed: ";
	int r, c;
	cin >> r >> c;
	return { r - 1,c - 1 };
}
Board::Board() { //Board initailization
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			board[i][j] = ' ';
		}
	}
	turn = 'O';
}

void Board::setInput(unique_ptr<Input>&& x, unique_ptr<Input>&& o) {
	xInput = move(x); //sets the inputs for the board
	oInput = move(o);
}
bool inRange(int x) {
	return 0 <= x && x < 3;
}
void Board::nextMove() {
	Pos p;
	if (turn == 'X') { //gets the next move from the input
		p = xInput->getPos();
	}
	else
		p = oInput->getPos();

	if (inRange(p.x) && inRange(p.y) && board[p.x][p.y] == ' ') {
		board[p.x][p.y] = turn;

		turn = (turn == 'X' ? 'O' : 'X');
		turncnt++;
	}
	else {
		cout << "\033[31mInvalid move\n\033[37m";
		Sleep(500);
	}
}
gameState Board::getState() { //Game win check
	bool gameOver = false;
	char whoWon;

	for (int i = 0; i < 3; i++) {
		bool rowWon = true;
		for (int j = 0; j < 2; j++) {
			if (board[i][j] == ' ' || board[i][j] != board[i][j + 1])rowWon = false;
		}
		if (rowWon) {
			gameOver = true;
			whoWon = board[i][0];
		}
	}
	for (int j = 0; j < 3; j++) {
		bool colWon = true;
		for (int i = 0; i < 2; i++) {
			if (board[i][j] == ' ' || board[i][j] != board[i + 1][j])colWon = false;
		}
		if (colWon) {
			gameOver = true;
			whoWon = board[0][j];
		}
	}
	bool diagonal1 = true, diagonal2 = true;
	for (int i = 0; i < 2; i++) {
		if (board[i][i] == ' ' || board[i][i] != board[i + 1][i + 1])diagonal1 = false;
		if (board[i][2 - i] == ' ' || board[i][2 - i] != board[i + 1][2 - i - 1])diagonal2 = false;
	}
	if (diagonal1 || diagonal2) {
		gameOver = true;
		whoWon = board[1][1];
	}

	if (gameOver) {
		if (whoWon == 'X')return X_won;
		else return O_won;
	}
	if (turncnt == 9)return Tie;
	return gameOngoing;
}


void Board::display() {
	cout << "Currently " << turn << "'s turn\n";

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			cout << board[i][j] << (j == 2 ? '\n' : '|');
		}
		cout << (i == 2 ? "\n" : "-+-+-\n");
	}
}

class Game { //Game class which operates with the board
	unique_ptr<Board> gameBoard;
	State state;
public:
	void start();
	void displayBoard();
};

void Game::displayBoard() {
	while (gameBoard->getState() == gameState::gameOngoing) {
		cout << "\033[2J\033[H"; //Move cursor to start
		gameBoard->display();
		gameBoard->nextMove();
	}
	cout << "\033[2J\033[H";
	gameBoard->display();
	//End game message
	if (gameBoard->getState() == O_won)
		cout << "O won!\n";
	else if (gameBoard->getState() == X_won)
		cout << "X won!\n";
	else if(gameBoard->getState() == Tie)
		cout << "It's a tie!\n";
}
void Game::start() {
	if (state == main_menu) {
		cout << "Welcome to tic tac toe\n";
		cout << "Choose to play against a friend (type 1), or against a random move ai (type 2)\n";
		int inp;
		cin >> inp;
		if (inp == 1) {
			gameBoard = make_unique<Board>();
			gameBoard->setInput(make_unique<humanInput>(), make_unique<humanInput>());
		}
		else {
			unique_ptr<random> tmp = make_unique<random>();
			gameBoard = make_unique<Board>();
			tmp->init_board(gameBoard.get());
			gameBoard->setInput(make_unique<humanInput>(), move(tmp));
		}
		state = play_game;
		start();
	}
	else if (state == play_game) {
		displayBoard();
	}

}



int main() {
	srand(time(0));

	Game g;

	g.start();

}
