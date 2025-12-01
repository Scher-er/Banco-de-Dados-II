import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class JogoDaVelhaRede extends JFrame {

    // Componentes da Interface
    private JButton[][] botoes = new JButton[3][3];
    private JLabel labelStatus;
    private JMenuItem itemCriar, itemConectar, itemSair;

    // Lógica do Jogo
    private boolean meuTurno = false;
    private String minhaMarca = null;      // "X" ou "O"
    private String marcaOponente = null;   // "O" ou "X"
    private boolean jogoAtivo = false;

    // Rede
    private Socket socket;
    private PrintWriter saida;
    private BufferedReader entrada;
    private ServerSocket serverSocket; // Usado apenas se for Host

    public JogoDaVelhaRede() {
        super("Jogo da Velha - Rede TCP");
        configurarInterface();
        setSize(400, 450);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // Centralizar na tela
        setResizable(false);
    }

    private void configurarInterface() {
        // Menu
        JMenuBar menuBar = new JMenuBar();
        JMenu menuJogo = new JMenu("Jogo / Conexão");
        
        itemCriar = new JMenuItem("Criar Servidor (Ser o X)");
        itemConectar = new JMenuItem("Conectar a um Jogo (Ser o O)");
        itemSair = new JMenuItem("Sair");

        itemCriar.addActionListener(e -> iniciarServidor());
        itemConectar.addActionListener(e -> conectarCliente());
        itemSair.addActionListener(e -> System.exit(0));

        menuJogo.add(itemCriar);
        menuJogo.add(itemConectar);
        menuJogo.addSeparator();
        menuJogo.add(itemSair);
        menuBar.add(menuJogo);
        setJMenuBar(menuBar);

        // Layout Principal
        setLayout(new BorderLayout());

        // Status
        labelStatus = new JLabel("Escolha uma opção no menu para começar...");
        labelStatus.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        labelStatus.setFont(new Font("Arial", Font.BOLD, 14));
        labelStatus.setHorizontalAlignment(SwingConstants.CENTER);
        add(labelStatus, BorderLayout.SOUTH);

        // Tabuleiro
        JPanel panelTabuleiro = new JPanel();
        panelTabuleiro.setLayout(new GridLayout(3, 3));
        
        Font fonteBotao = new Font("Arial", Font.BOLD, 60);

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                JButton btn = new JButton("");
                btn.setFont(fonteBotao);
                btn.setFocusPainted(false);
                final int r = i;
                final int c = j;

                // Evento de clique no botão do tabuleiro
                btn.addActionListener(e -> realizarJogada(r, c));
                
                botoes[i][j] = btn;
                panelTabuleiro.add(btn);
            }
        }
        add(panelTabuleiro, BorderLayout.CENTER);
        
        bloquearTabuleiro(); // Começa bloqueado até conectar
    }

    // --- LÓGICA DE REDE ---

    private void iniciarServidor() {
        new Thread(() -> {
            try {
                // Porta fixa para simplificar (poderia ser input do usuário)
                int porta = 12345; 
                serverSocket = new ServerSocket(porta);
                
                SwingUtilities.invokeLater(() -> {
                    labelStatus.setText("Aguardando oponente na porta " + porta + "...");
                    setTitle("Jogo da Velha (Host - Jogador X)");
                    itemCriar.setEnabled(false);
                    itemConectar.setEnabled(false);
                });

                // Bloqueia até um cliente conectar
                socket = serverSocket.accept();
                configurarStreams(socket, "X");

            } catch (IOException ex) {
                ex.printStackTrace();
                JOptionPane.showMessageDialog(this, "Erro ao iniciar servidor: " + ex.getMessage());
            }
        }).start();
    }

    private void conectarCliente() {
        String ip = JOptionPane.showInputDialog(this, "Digite o IP do servidor:", "localhost");
        if (ip == null || ip.trim().isEmpty()) return;

        new Thread(() -> {
            try {
                int porta = 12345;
                socket = new Socket(ip, porta);
                
                SwingUtilities.invokeLater(() -> {
                    setTitle("Jogo da Velha (Cliente - Jogador O)");
                    itemCriar.setEnabled(false);
                    itemConectar.setEnabled(false);
                });

                configurarStreams(socket, "O");

            } catch (IOException ex) {
                ex.printStackTrace();
                JOptionPane.showMessageDialog(this, "Erro ao conectar: " + ex.getMessage());
            }
        }).start();
    }

    private void configurarStreams(Socket socket, String marca) throws IOException {
        saida = new PrintWriter(socket.getOutputStream(), true);
        entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        
        this.minhaMarca = marca;
        this.marcaOponente = marca.equals("X") ? "O" : "X";
        this.jogoAtivo = true;

        // Quem é X começa
        if (marca.equals("X")) {
            meuTurno = true;
            SwingUtilities.invokeLater(() -> {
                labelStatus.setText("Conectado! Sua vez (X)");
                desbloquearTabuleiro();
            });
        } else {
            meuTurno = false;
            SwingUtilities.invokeLater(() -> {
                labelStatus.setText("Conectado! Aguardando oponente (X)...");
                bloquearTabuleiro(); // Garante que começa bloqueado
            });
        }

        // Inicia a Thread que fica ouvindo as mensagens do oponente
        new Thread(new ReceptorMensagens()).start();
    }

    // --- LÓGICA DO JOGO ---

    private void realizarJogada(int r, int c) {
        // Validações locais
        if (!jogoAtivo || !meuTurno) return;
        if (!botoes[r][c].getText().equals("")) return;

        // 1. Atualiza visualmente local
        botoes[r][c].setText(minhaMarca);
        botoes[r][c].setForeground(Color.BLUE); // Minha cor
        
        // 2. Envia protocolo para o oponente: MOVE linha coluna
        saida.println("MOVE " + r + " " + c);

        // 3. Verifica estado do jogo
        if (verificarVitoria(minhaMarca)) {
            labelStatus.setText("VOCÊ VENCEU!");
            saida.println("GAMEOVER PERDEU"); 
            jogoAtivo = false;
            bloquearTabuleiro();
        } else if (verificarEmpate()) {
            labelStatus.setText("EMPATE!");
            saida.println("GAMEOVER EMPATE");
            jogoAtivo = false;
        } else {
            // Passa a vez
            meuTurno = false;
            labelStatus.setText("Aguardando jogada do oponente...");
            bloquearTabuleiro();
        }
    }

    private void processarJogadaOponente(int r, int c) {
        SwingUtilities.invokeLater(() -> {
            botoes[r][c].setText(marcaOponente);
            botoes[r][c].setForeground(Color.RED); // Cor do oponente
            
          
            meuTurno = true;
            labelStatus.setText("Sua vez! (" + minhaMarca + ")");
            desbloquearTabuleiro();
        });
    }

    // --- CLASSE INTERNA: LISTENER DE REDE ---
    // Fica rodando em background para receber comandos do socket
    private class ReceptorMensagens implements Runnable {
        @Override
        public void run() {
            try {
                String linha;
                while ((linha = entrada.readLine()) != null) {
                    // Protocolo simples via texto
                    if (linha.startsWith("MOVE")) {
                        String[] partes = linha.split(" ");
                        int r = Integer.parseInt(partes[1]);
                        int c = Integer.parseInt(partes[2]);
                        processarJogadaOponente(r, c);
                    } 
                    else if (linha.startsWith("GAMEOVER")) {
                        String resultado = linha.split(" ")[1]; // PERDEU ou EMPATE
                        jogoAtivo = false;
                        SwingUtilities.invokeLater(() -> {
                            if (resultado.equals("PERDEU")) {
                                labelStatus.setText("VOCÊ PERDEU! O oponente venceu.");
                            } else {
                                labelStatus.setText("EMPATE!");
                            }
                            bloquearTabuleiro();
                        });
                        
                        break;
                    }
                }
            } catch (IOException e) {
                if (jogoAtivo) { // Se não foi logout intencional
                    SwingUtilities.invokeLater(() -> {
                        JOptionPane.showMessageDialog(JogoDaVelhaRede.this, "Oponente desconectou.");
                        labelStatus.setText("Conexão perdida.");
                        bloquearTabuleiro();
                    });
                }
            }
        }
    }

    // --- UTILITÁRIOS ---

    private boolean verificarVitoria(String marca) {
        // Linhas e Colunas
        for (int i = 0; i < 3; i++) {
            if (checar(i,0, i,1, i,2, marca)) return true;
            if (checar(0,i, 1,i, 2,i, marca)) return true;
        }
        // Diagonais
        if (checar(0,0, 1,1, 2,2, marca)) return true;
        if (checar(0,2, 1,1, 2,0, marca)) return true;
        
        return false;
    }

    private boolean checar(int r1, int c1, int r2, int c2, int r3, int c3, String marca) {
        return botoes[r1][c1].getText().equals(marca) &&
               botoes[r2][c2].getText().equals(marca) &&
               botoes[r3][c3].getText().equals(marca);
    }

    private boolean verificarEmpate() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (botoes[i][j].getText().isEmpty()) return false;
            }
        }
        return true;
    }

    private void bloquearTabuleiro() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                botoes[i][j].setEnabled(false);
            }
        }
    }

    private void desbloquearTabuleiro() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                // Só habilita células vazias
                if (botoes[i][j].getText().isEmpty()) {
                    botoes[i][j].setEnabled(true);
                }
            }
        }
    }

    public static void main(String[] args) {
        // Garante que a GUI seja criada na Thread correta do Swing
        SwingUtilities.invokeLater(() -> {
            new JogoDaVelhaRede().setVisible(true);
        });
    }
}