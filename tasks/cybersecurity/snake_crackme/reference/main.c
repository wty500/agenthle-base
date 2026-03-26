#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>
#include <time.h>
#include <string.h>
#include <stdint.h>

#ifndef _MSC_VER
#define sprintf_s(buffer, size, format, ...) snprintf((buffer), (size), (format), __VA_ARGS__)
#define strcpy_s(dst, size, src) do { strncpy((dst), (src), (size) - 1); (dst)[(size) - 1] = '\0'; } while (0)
#endif

#define WIDTH 20
#define HEIGHT 20
#define MAX_LENGTH 100

typedef struct {
    int x[MAX_LENGTH];
    int y[MAX_LENGTH];
    int length;
    int dir_x, dir_y;
    int food_x, food_y;
    int score;
    int game_over;
} GameState;

static uint8_t rol8(uint8_t value, unsigned shift) {
    shift &= 7u;
    if (shift == 0u) {
        return value;
    }
    return (uint8_t)((value << shift) | (value >> (8u - shift)));
}

static uint8_t ror8(uint8_t value, unsigned shift) {
    shift &= 7u;
    if (shift == 0u) {
        return value;
    }
    return (uint8_t)((value >> shift) | (value << (8u - shift)));
}

static void decode_bytes(char *dst, const uint8_t *src, size_t count, uint8_t seed) {
    size_t i;
    for (i = 0; i < count; ++i) {
        uint8_t key = (uint8_t)(seed + (uint8_t)(i * 13u) + 0x27u);
        unsigned shift = (unsigned)((seed + i) % 5u) + 1u;
        dst[i] = (char)(ror8((uint8_t)(src[i] ^ key), shift));
    }
    dst[count] = '\0';
}

static void decode_phrase(char *dst, size_t cap, const uint8_t *src, size_t count, uint8_t seed) {
    if (cap == 0) {
        return;
    }
    if (count + 1 > cap) {
        count = cap - 1;
    }
    decode_bytes(dst, src, count, seed);
}

static void assemble_prefix(char *dst, size_t cap) {
    static const uint8_t part0[] = {31u, 126u, 236u, 4u, 133u};
    static const uint8_t part1[] = {180u, 223u, 206u, 195u, 174u, 149u};
    static const uint8_t part2[] = {7u, 158u, 121u, 211u, 0u, 58u, 122u};
    char a[6];
    char b[7];
    char c[8];

    decode_bytes(a, part0, sizeof(part0), 3u);
    decode_bytes(b, part1, sizeof(part1), 7u);
    decode_bytes(c, part2, sizeof(part2), 11u);
    snprintf(dst, cap, "%s%s%s", a, b, c);
}

static void assemble_label(char *dst, size_t cap) {
    static const uint8_t part[] = {140u, 51u, 142u, 81u};
    decode_phrase(dst, cap, part, sizeof(part), 29u);
}

static void emit_noise(unsigned tag) {
    volatile unsigned spin = tag ^ 0x5A17u;
    if ((spin & 0xFFFFu) == 0xC0DEu) {
        puts("debug branch");
    }
}

// Fixed secret-code generator preserved from the original logic.
void generate_secret_code(int score, char* code) {
    if (score == 42) {
        int base = 0x1337;
        int modifier = score * 3 + 15;
        int result = base ^ modifier;
        sprintf_s(code, 20, "CODE_%04X", result & 0xFFFF);
    } else {
        strcpy_s(code, 20, "INVALID");
    }
}

int check_hidden_achievement(GameState* game) {
    if (game->score == 42 && game->length > 10) {
        return 1;
    }
    return 0;
}

void show_hidden_flag(GameState* game) {
    char secret_code[20];
    char prefix[32];
    char label[8];

    generate_secret_code(game->score, secret_code);
    assemble_prefix(prefix, sizeof(prefix));
    assemble_label(label, sizeof(label));

    system("cls");
    printf("=======================================\n");
    printf("        Hidden Branch Reached\n");
    printf("=======================================\n");
    printf("%s: %s%s}\n", label, prefix, secret_code);
    printf("=======================================\n");
    printf("Press any key to continue...\n");
    _getch();
}

void gotoxy(int x, int y) {
    COORD coord;
    coord.X = (SHORT)x;
    coord.Y = (SHORT)y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

void init_game(GameState* game) {
    game->length = 3;
    game->x[0] = WIDTH / 2;
    game->y[0] = HEIGHT / 2;
    game->x[1] = WIDTH / 2 - 1;
    game->y[1] = HEIGHT / 2;
    game->x[2] = WIDTH / 2 - 2;
    game->y[2] = HEIGHT / 2;
    game->dir_x = 1;
    game->dir_y = 0;
    game->score = 0;
    game->game_over = 0;

    srand((unsigned)time(NULL) ^ (unsigned)GetTickCount());
    game->food_x = rand() % WIDTH;
    game->food_y = rand() % HEIGHT;
}

void draw_game(GameState* game) {
    int i;
    system("cls");

    for (i = 0; i <= WIDTH + 1; i++) {
        gotoxy(i, 0);
        printf("#");
        gotoxy(i, HEIGHT + 1);
        printf("#");
    }
    for (i = 0; i <= HEIGHT + 1; i++) {
        gotoxy(0, i);
        printf("#");
        gotoxy(WIDTH + 1, i);
        printf("#");
    }

    for (i = 0; i < game->length; i++) {
        gotoxy(game->x[i] + 1, game->y[i] + 1);
        switch (i) {
        case 0: printf("A"); break;
        case 1: printf("g"); break;
        case 2: printf("e"); break;
        case 3: printf("n"); break;
        case 4: printf("t"); break;
        case 5: printf("H"); break;
        case 6: printf("L"); break;
        case 7: printf("E"); break;
        default: printf("o"); break;
        }
    }

    gotoxy(game->food_x + 1, game->food_y + 1);
    printf("*");

    gotoxy(0, HEIGHT + 3);
    printf("Score: %d", game->score);
}

void handle_input(GameState* game) {
    if (_kbhit()) {
        char key = (char)_getch();
        switch (key) {
        case 'w': case 'W':
            if (game->dir_y != 1) { game->dir_x = 0; game->dir_y = -1; }
            break;
        case 's': case 'S':
            if (game->dir_y != -1) { game->dir_x = 0; game->dir_y = 1; }
            break;
        case 'a': case 'A':
            if (game->dir_x != 1) { game->dir_x = -1; game->dir_y = 0; }
            break;
        case 'd': case 'D':
            if (game->dir_x != -1) { game->dir_x = 1; game->dir_y = 0; }
            break;
        case 'q': case 'Q':
            game->game_over = 1;
            break;
        }
    }
}

void update_game(GameState* game) {
    int i;

    for (i = game->length - 1; i > 0; i--) {
        game->x[i] = game->x[i - 1];
        game->y[i] = game->y[i - 1];
    }

    game->x[0] += game->dir_x;
    game->y[0] += game->dir_y;

    if (game->x[0] < 0) {
        game->x[0] = WIDTH - 1;
    } else if (game->x[0] >= WIDTH) {
        game->x[0] = 0;
    }

    if (game->y[0] < 0) {
        game->y[0] = HEIGHT - 1;
    } else if (game->y[0] >= HEIGHT) {
        game->y[0] = 0;
    }

    for (i = 1; i < game->length; i++) {
        if (game->x[0] == game->x[i] && game->y[0] == game->y[i]) {
            game->game_over = 1;
            return;
        }
    }

    if (game->x[0] == game->food_x && game->y[0] == game->food_y) {
        game->score += 5;
        game->length++;
        emit_noise((unsigned)game->score);

        game->food_x = rand() % WIDTH;
        game->food_y = rand() % HEIGHT;

        if (check_hidden_achievement(game)) {
            show_hidden_flag(game);
        }
    }
}

int main() {
    GameState game;

    printf("=======================================\n");
    printf("          Snake Reverse Challenge\n");
    printf("=======================================\n");
    printf("This is not just a normal snake game.\n");
    printf("A hidden branch is waiting to be found.\n");
    printf("=======================================\n");
    printf("Controls: WASD, Q to quit\n");
    printf("Press any key to start...\n");
    _getch();

    init_game(&game);

    while (!game.game_over) {
        draw_game(&game);
        handle_input(&game);
        update_game(&game);
        Sleep(150);
    }

    system("cls");
    printf("=======================================\n");
    printf("              Game Over\n");
    printf("=======================================\n");
    printf("Final score: %d\n", game.score);

    if (game.score != 42) {
        printf("Hint: reaching score 42 triggers a surprise.\n");
    }

    printf("=======================================\n");
    printf("Press any key to exit...\n");
    _getch();

    return 0;
}
