;; Derived from https://gist.github.com/pnf/5924614


;; Utilities

(defn average [ns]
  (/ (reduce + ns) (count ns)))

;; XXX I'm a clojure beginner, how can this be nicer or avoided?
(defn mins-key
  "Returns the x's for which (key x) is leest. (One or more of them)."
  [key x & more]
  (if (empty? more)
      (list x)
      (let [mins (apply mins-key key more)
            x-k (key x)
            min-k (key (first mins))]
        (cond (< min-k x-k) mins
              (= min-k x-k) (cons x mins)
              :else         (list x)))))


;; Bit-board representation: a pair of bitsets [p q], p for the
;; player to move, q for their opponent. The least significant bit is
;; the lower-right square; msb is upper-left. (Differs from the human
;; move numbering for the sake of nice octal constants.)

(def empty-grid [0 0])

(defn full?
  "Is no move possible?"
  [[p q]]
  (= 0777 (bit-or p q)))

(def ways-to-win [0700 0070 0007 0444 0222 0111 0421 0124])

(defn won?
  "Did the previous move win the game?"
  [[p q]]
  (some #(= (bit-and q %) %) ways-to-win))

(defn apply-move [[p q] move]
  (let [square (bit-shift-left 1 move)]
    (and (= 0 (bit-and square (bit-or p q)))
         [q (bit-or p square)])))

(defn successors
  "Make all valid moves on grid."
  [grid]
  (filter identity (map #(apply-move grid %) (range 9))))

(defn pretty [[p q] [p-mark q-mark]]
  (map (fn [square]
         (cond (pos? (bit-and p square)) p-mark
               (pos? (bit-and q square)) q-mark
               :else                     "."))
       (map #(bit-shift-left 1 %) (reverse (range 9)))))

(defn print-board [grid marks]
  (doseq [row (re-seq #"..." (apply str (pretty grid marks)))]
    (println row)))


;; Values and moves

(def drunk-value
  (memoize
   (fn [grid]
     (cond (won? grid) -1
           (full? grid) 0
           :else (- (float (average (map drunk-value (successors grid)))))))))

(def value
  (memoize
   (fn [grid]
     (cond (won? grid) -1
           (full? grid) 0
           :else (- (reduce min (map value (successors grid))))))))

;; Pre: the game's not over
(defn pick-successor
  "Make a best move, breaking ties by best average value."
  [grid]
  (apply min-key drunk-value
         (apply mins-key value (successors grid))))
