import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Collapse,
  IconButton,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { PracticeProblem } from '../types/studyBuddy';

interface PracticeProblemProps {
  problem: PracticeProblem;
  onAnswer: (isCorrect: boolean) => void;
}

const PracticeProblemComponent: React.FC<PracticeProblemProps> = ({
  problem,
  onAnswer,
}) => {
  const [answer, setAnswer] = useState('');
  const [showExplanation, setShowExplanation] = useState(false);
  const [isAnswered, setIsAnswered] = useState(false);

  const handleSubmit = () => {
    const isCorrect = answer.toLowerCase() === problem.answer.toLowerCase();
    setIsAnswered(true);
    onAnswer(isCorrect);
  };

  const renderAnswerInput = () => {
    switch (problem.question_type) {
      case 'multiple_choice':
        return (
          <FormControl component="fieldset">
            <FormLabel component="legend">Select your answer:</FormLabel>
            <RadioGroup
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            >
              {problem.answer.split(',').map((option, index) => (
                <FormControlLabel
                  key={index}
                  value={option.trim()}
                  control={<Radio />}
                  label={option.trim()}
                  disabled={isAnswered}
                />
              ))}
            </RadioGroup>
          </FormControl>
        );
      case 'free_response':
        return (
          <TextField
            fullWidth
            multiline
            rows={4}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            label="Your answer"
            disabled={isAnswered}
          />
        );
      case 'coding':
        return (
          <TextField
            fullWidth
            multiline
            rows={8}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            label="Your code"
            disabled={isAnswered}
          />
        );
      default:
        return null;
    }
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {problem.topic} - {problem.difficulty}
        </Typography>
        <Typography variant="body1" paragraph>
          {problem.question_text}
        </Typography>

        {renderAnswerInput()}

        <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!answer || isAnswered}
          >
            Submit Answer
          </Button>
          {isAnswered && (
            <Button
              variant="outlined"
              onClick={() => setShowExplanation(!showExplanation)}
              endIcon={<ExpandMoreIcon />}
            >
              {showExplanation ? 'Hide Explanation' : 'Show Explanation'}
            </Button>
          )}
        </Box>

        <Collapse in={showExplanation}>
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Explanation:
            </Typography>
            <Typography variant="body2">{problem.explanation}</Typography>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default PracticeProblemComponent; 