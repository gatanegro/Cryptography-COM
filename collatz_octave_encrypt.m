% Collatz-Octave Cryptographic Transformation
% This script encrypts numbers using recursive Collatz-Octave scaling.

function encrypted_sequence = collatz_octave_encrypt(n, key, steps)
    % n     = initial number
    % key   = secret key shift in transformation
    % steps = number of iterations

    encrypted_sequence = []; % Store encrypted values

    for i = 1:steps
        if mod(n, 2) == 0
            n = n / 2;  % Even step
        else
            n = 3 * n + key;  % Odd step with key modification
        end

        % Reduce to single-digit octave sum
        reduced_value = mod(sum(arrayfun(@(c) str2num(c), num2str(n))), 9) + 1;
        encrypted_sequence = [encrypted_sequence, reduced_value];

        % Stop if we reach a repeating pattern (prevention)
        if length(encrypted_sequence) > 1 && encrypted_sequence(end) == encrypted_sequence(end-1)
            break;
        end
    end
end

% Example Usage
initial_number = 27;  % Starting number for encryption
encryption_key = 5;   % Secret key
num_steps = 15;       % Number of iterations

% Run the encryption
result = collatz_octave_encrypt(initial_number, encryption_key, num_steps);

% Display results
disp('Collatz-Octave Encrypted Sequence:')
disp(result)

